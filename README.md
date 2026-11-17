# Hucha web (para instalar en el iPhone sin Mac)

La misma app en versión web. Se instala en la pantalla de inicio del iPhone desde Safari,
se abre a pantalla completa y funciona sin conexión.

## Qué hay en esta carpeta

- `index.html`: la app entera (interfaz y lógica).
- `manifest.webmanifest`, `sw.js` e `icons/`: lo que hace que se instale y funcione sin conexión.

## Ponerla en tu iPhone con GitHub Pages (gratis)

1. En GitHub crea un repositorio público, por ejemplo `hucha`.
2. Sube **el contenido de esta carpeta** (no la carpeta en sí): `index.html`, `sw.js`,
   `manifest.webmanifest` y la carpeta `icons`.
3. En el repositorio: **Settings → Pages → Build and deployment → Deploy from a branch**,
   rama `main`, carpeta `/ (root)` y **Save**.
4. Al cabo de un minuto estará en `https://TU_USUARIO.github.io/hucha/`.
5. Abre esa dirección en **Safari** en el iPhone → botón **Compartir** →
   **Añadir a pantalla de inicio**.

Vale cualquier otro alojamiento de archivos estáticos con HTTPS.

## Dónde se guardan los datos

En el propio iPhone, dentro de la app instalada. En GitHub solo está el código: tus gastos
no salen del teléfono.

Haz una copia de vez en cuando en **Ajustes → Exportar copia**. Ese archivo `.json` se
puede importar también en la app nativa de iPhone, y al revés.

## Probarla en el ordenador

Desde esta carpeta:

```
python -m http.server 8000
```

y abre `http://localhost:8000`.
