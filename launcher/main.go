// Kenti por grupo taxonómico — versión de escritorio.
//
// El programa sirve la interfaz (embebida) en 127.0.0.1 y la abre en una
// ventana propia de Edge o Chrome. Los datos se guardan en un archivo JSON en
// Documentos\<carpeta del grupo>. Sin dependencias externas: sólo la
// biblioteca estándar de Go.
package main

import (
	"bytes"
	"embed"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"log"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"time"
)

//go:embed web
var webFS embed.FS

const version = "0.5"

// Valores por grupo taxonómico: se fijan al compilar con -ldflags "-X main.appID=...".
var (
	appID      = "kenti-macroinvertebrados"
	appName    = "Kenti Macroinvertebrados"
	folderName = "Kenti Macroinvertebrados"
	dataName   = "datos-macroinvertebrados.json"
	portText   = "47837"
)

var (
	preferredPort int
	dataDir       string
	dataFile      string
	saveMu        sync.Mutex
	backedUp      bool
	pingMu        sync.Mutex
	lastPing      = time.Now()
	listenAddr    string
)

// Cada referencia en su propio archivo: el archivo de datos, que se comparte
// con el administrador, queda en unos pocos KB.
var refFiles = map[string]string{
	"dic": "referencia-omnidia.json",
	"ibd": "referencia-ibd.json",
}

func main() {
	if p, err := strconv.Atoi(portText); err == nil {
		preferredPort = p
	} else {
		preferredPort = 47837
	}
	dataDir = filepath.Join(documentsDir(), folderName)
	if err := os.MkdirAll(dataDir, 0o755); err != nil {
		fatal("No se pudo crear la carpeta de datos:\n" + dataDir + "\n\n" + err.Error())
	}
	dataFile = filepath.Join(dataDir, dataName)
	if lf, err := os.OpenFile(filepath.Join(dataDir, "kenti.log"), os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0o644); err == nil {
		log.SetOutput(lf)
		defer lf.Close()
	}

	ln, err := net.Listen("tcp", fmt.Sprintf("127.0.0.1:%d", preferredPort))
	if err != nil {
		// ¿Ya hay un Kenti abierto? Entonces sólo abrimos otra ventana.
		if kentiRunning(preferredPort) {
			log.Println("Kenti ya estaba abierto; se abre otra ventana")
			openWindow(fmt.Sprintf("http://127.0.0.1:%d/", preferredPort))
			return
		}
		ln, err = net.Listen("tcp", "127.0.0.1:0")
		if err != nil {
			fatal("Kenti no pudo iniciar su servidor local.\n\n" + err.Error())
		}
	}
	listenAddr = ln.Addr().String()
	url := "http://" + listenAddr + "/"

	srv := &http.Server{Handler: routes(), ReadHeaderTimeout: 10 * time.Second}
	go func() {
		if err := srv.Serve(ln); err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.Println("servidor:", err)
		}
	}()
	log.Printf("%s %s en %s · datos: %s", appName, version, url, dataFile)

	if done := openWindow(url); done != nil {
		<-done // la ventana se cerró
		time.Sleep(1200 * time.Millisecond)
	} else {
		// Navegador predeterminado: se cierra tras 3 minutos sin señales de la página.
		for {
			time.Sleep(30 * time.Second)
			pingMu.Lock()
			idle := time.Since(lastPing)
			pingMu.Unlock()
			if idle > 3*time.Minute {
				break
			}
		}
	}
	log.Println("Kenti se cerró")
}

func kentiRunning(port int) bool {
	c := http.Client{Timeout: 2 * time.Second}
	r, err := c.Get(fmt.Sprintf("http://127.0.0.1:%d/api/info", port))
	if err != nil {
		return false
	}
	defer r.Body.Close()
	var info map[string]any
	return json.NewDecoder(r.Body).Decode(&info) == nil && info["app"] == appID
}

func routes() http.Handler {
	sub, _ := fs.Sub(webFS, "web")
	static := http.FileServer(http.FS(sub))
	mux := http.NewServeMux()

	mux.HandleFunc("/api/info", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]any{"app": appID, "version": version, "carpeta": dataDir, "archivo": dataFile})
	})
	mux.HandleFunc("/api/ping", func(w http.ResponseWriter, r *http.Request) {
		pingMu.Lock()
		lastPing = time.Now()
		pingMu.Unlock()
		writeJSON(w, map[string]any{"ok": true})
	})
	mux.HandleFunc("/api/datos", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			b, err := os.ReadFile(dataFile)
			if errors.Is(err, os.ErrNotExist) {
				w.WriteHeader(http.StatusNoContent) // todavía no hay datos guardados
				return
			} else if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			w.Header().Set("Content-Type", "application/json; charset=utf-8")
			w.Write(b)
		case http.MethodPut, http.MethodPost:
			if !trusted(r) {
				http.Error(w, "origen no permitido", http.StatusForbidden)
				return
			}
			b, err := io.ReadAll(io.LimitReader(r.Body, 64<<20))
			if err != nil || !json.Valid(b) {
				http.Error(w, "datos inválidos", http.StatusBadRequest)
				return
			}
			if err := saveData(b); err != nil {
				log.Println("guardar:", err)
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			writeJSON(w, map[string]any{"ok": true})
		default:
			http.Error(w, "método no permitido", http.StatusMethodNotAllowed)
		}
	})
	// Las referencias de diatomeas: diccionario (código ↔ nombre) y perfiles del
	// IBD. Cada una en su archivo, fuera del archivo de datos.
	mux.HandleFunc("/api/referencia", func(w http.ResponseWriter, r *http.Request) {
		if !trusted(r) {
			http.Error(w, "origen no permitido", http.StatusForbidden)
			return
		}
		switch r.Method {
		case http.MethodGet:
			out := map[string]any{}
			for tipo, name := range refFiles {
				b, err := os.ReadFile(filepath.Join(dataDir, name))
				if err != nil || !json.Valid(b) {
					out[tipo] = nil
					continue
				}
				out[tipo] = json.RawMessage(b)
			}
			w.Header().Set("Content-Type", "application/json; charset=utf-8")
			json.NewEncoder(w).Encode(out)
		case http.MethodPut, http.MethodPost:
			tipo := r.URL.Query().Get("tipo")
			name, ok := refFiles[tipo]
			if !ok {
				http.Error(w, "tipo de referencia desconocido", http.StatusBadRequest)
				return
			}
			b, err := io.ReadAll(io.LimitReader(r.Body, 128<<20))
			if err != nil || !json.Valid(b) {
				http.Error(w, "referencia inválida", http.StatusBadRequest)
				return
			}
			path := filepath.Join(dataDir, name)
			if bytes.Equal(bytes.TrimSpace(b), []byte("null")) {
				os.Remove(path)
				writeJSON(w, map[string]any{"ok": true})
				return
			}
			saveMu.Lock()
			err = writeAtomic(path, b)
			saveMu.Unlock()
			if err != nil {
				log.Println("guardar referencia:", err)
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			writeJSON(w, map[string]any{"ok": true})
		default:
			http.Error(w, "método no permitido", http.StatusMethodNotAllowed)
		}
	})
	mux.HandleFunc("/api/taxon", func(w http.ResponseWriter, r *http.Request) {
		if !trusted(r) {
			http.Error(w, "origen no permitido", http.StatusForbidden)
			return
		}
		writeJSON(w, taxonLookup(r.URL.Query().Get("nombre"), r.URL.Query().Get("genero"), r.URL.Query().Get("especie"), reinoValido(r.URL.Query().Get("reino"))))
	})
	// El Excel lo arma la página; el lanzador sólo lo guarda en la carpeta de datos.
	mux.HandleFunc("/api/exportar", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost || !trusted(r) {
			http.Error(w, "no permitido", http.StatusForbidden)
			return
		}
		b, err := io.ReadAll(io.LimitReader(r.Body, 256<<20))
		if err != nil || len(b) == 0 {
			http.Error(w, "no llegó el archivo", http.StatusBadRequest)
			return
		}
		name := safeName(r.URL.Query().Get("nombre"))
		if name == "" {
			name = "Kenti"
		}
		final := name + ".xlsx"
		path := filepath.Join(dataDir, final)
		for i := 2; i < 200; i++ {
			if _, err := os.Stat(path); errors.Is(err, os.ErrNotExist) {
				break
			}
			final = fmt.Sprintf("%s (%d).xlsx", name, i)
			path = filepath.Join(dataDir, final)
		}
		saveMu.Lock()
		err = writeAtomic(path, b)
		saveMu.Unlock()
		if err != nil {
			log.Println("exportar:", err)
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		writeJSON(w, map[string]any{"ok": true, "nombre": final, "carpeta": dataDir})
	})
	mux.HandleFunc("/api/abrir-exportacion", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost || !trusted(r) {
			http.Error(w, "no permitido", http.StatusForbidden)
			return
		}
		var q struct{ Nombre, Modo string }
		json.NewDecoder(io.LimitReader(r.Body, 1<<16)).Decode(&q)
		name := safeName(strings.TrimSuffix(q.Nombre, ".xlsx"))
		if name == "" {
			http.Error(w, "nombre inválido", http.StatusBadRequest)
			return
		}
		path := filepath.Join(dataDir, name+".xlsx")
		if q.Modo == "abrir" {
			openFile(path)
		} else {
			openFolder(dataDir)
		}
		writeJSON(w, map[string]any{"ok": true})
	})
	mux.HandleFunc("/api/abrir-carpeta", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost || !trusted(r) {
			http.Error(w, "no permitido", http.StatusForbidden)
			return
		}
		openFolder(dataDir)
		writeJSON(w, map[string]any{"ok": true})
	})
	mux.Handle("/", static)

	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Sólo se atiende a esta máquina con su propio nombre de host (evita DNS rebinding).
		if !localHost(r.Host) {
			http.Error(w, "host no permitido", http.StatusForbidden)
			return
		}
		w.Header().Set("Cache-Control", "no-store")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		mux.ServeHTTP(w, r)
	})
}

var nameBad = regexp.MustCompile(`[^\p{L}\p{N} ._()-]+`)

// safeName deja un nombre de archivo sin rutas ni caracteres raros.
func safeName(s string) string {
	s = strings.TrimSpace(nameBad.ReplaceAllString(s, " "))
	s = strings.Trim(strings.Join(strings.Fields(s), " "), " .")
	if len(s) > 120 {
		s = strings.TrimSpace(s[:120])
	}
	return s
}

func localHost(host string) bool {
	h, _, err := net.SplitHostPort(host)
	if err != nil {
		h = host
	}
	return h == "127.0.0.1" || h == "localhost"
}

// trusted exige la cabecera propia de Kenti: un sitio web ajeno no puede
// enviarla sin una verificación CORS que este servidor nunca aprueba.
func trusted(r *http.Request) bool {
	if r.Header.Get("X-Kenti") != "1" {
		return false
	}
	if o := r.Header.Get("Origin"); o != "" && !strings.HasPrefix(o, "http://127.0.0.1:") && !strings.HasPrefix(o, "http://localhost:") {
		return false
	}
	return true
}

func writeAtomic(path string, b []byte) error {
	tmp := path + ".tmp"
	if err := os.WriteFile(tmp, b, 0o644); err != nil {
		return err
	}
	return os.Rename(tmp, path)
}

func saveData(b []byte) error {
	saveMu.Lock()
	defer saveMu.Unlock()
	// Una copia de respaldo del archivo anterior, una vez por sesión.
	if !backedUp {
		if old, err := os.ReadFile(dataFile); err == nil && len(old) > 0 {
			_ = os.WriteFile(filepath.Join(dataDir, strings.TrimSuffix(dataName, ".json")+".respaldo.json"), old, 0o644)
		}
		backedUp = true
	}
	var pretty bytes.Buffer
	if err := json.Indent(&pretty, b, "", "  "); err != nil {
		return err
	}
	return writeAtomic(dataFile, pretty.Bytes())
}

// reinoValido deja pasar sólo los reinos que GBIF conoce.
func reinoValido(s string) string {
	switch s {
	case "Animalia", "Plantae", "Chromista", "Bacteria", "Protozoa", "Fungi":
		return s
	}
	return ""
}

func writeJSON(w http.ResponseWriter, v any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	json.NewEncoder(w).Encode(v)
}
