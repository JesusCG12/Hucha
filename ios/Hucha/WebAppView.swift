import SwiftUI
import UIKit
import WebKit

/// Muestra la app web incluida en la carpeta Web del paquete.
/// Se sirve con un esquema propio (hucha://app/) para que el almacenamiento local sea estable.
struct WebAppView: UIViewRepresentable {
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.websiteDataStore = .default()
        config.setURLSchemeHandler(context.coordinator, forURLScheme: Coordinator.scheme)
        config.userContentController.add(context.coordinator, name: "huchaSave")

        let web = WKWebView(frame: .zero, configuration: config)
        web.navigationDelegate = context.coordinator
        web.isOpaque = false
        web.backgroundColor = UIColor(named: "Papel")
        web.scrollView.backgroundColor = UIColor(named: "Papel")
        // La página ya respeta la isla dinámica y la barra de inicio con env(safe-area-inset-*).
        web.scrollView.contentInsetAdjustmentBehavior = .never
        web.scrollView.bounces = false
        web.allowsLinkPreview = false
        context.coordinator.webView = web

        if let start = URL(string: Coordinator.scheme + "://app/index.html") {
            web.load(URLRequest(url: start))
        }
        return web
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    final class Coordinator: NSObject, WKURLSchemeHandler, WKScriptMessageHandler, WKNavigationDelegate {
        static let scheme = "hucha"
        weak var webView: WKWebView?

        private var root: URL {
            Bundle.main.bundleURL.appendingPathComponent("Web", isDirectory: true)
        }

        // MARK: Archivos de la app (hucha://app/…)

        func webView(_ webView: WKWebView, start urlSchemeTask: WKURLSchemeTask) {
            guard let url = urlSchemeTask.request.url else {
                urlSchemeTask.didFailWithError(URLError(.badURL))
                return
            }
            var path = url.path
            if path.isEmpty || path == "/" {
                path = "/index.html"
            }
            let file = root.appendingPathComponent(String(path.dropFirst())).standardizedFileURL
            guard file.path.hasPrefix(root.standardizedFileURL.path),
                  let data = try? Data(contentsOf: file) else {
                urlSchemeTask.didFailWithError(URLError(.fileDoesNotExist))
                return
            }
            let headers = [
                "Content-Type": Coordinator.mimeType(for: file.pathExtension),
                "Content-Length": String(data.count),
                "Cache-Control": "no-cache"
            ]
            guard let response = HTTPURLResponse(url: url, statusCode: 200, httpVersion: "HTTP/1.1", headerFields: headers) else {
                urlSchemeTask.didFailWithError(URLError(.cannotParseResponse))
                return
            }
            urlSchemeTask.didReceive(response)
            urlSchemeTask.didReceive(data)
            urlSchemeTask.didFinish()
        }

        func webView(_ webView: WKWebView, stop urlSchemeTask: WKURLSchemeTask) {}

        static func mimeType(for ext: String) -> String {
            switch ext.lowercased() {
            case "html": return "text/html; charset=utf-8"
            case "js": return "text/javascript; charset=utf-8"
            case "css": return "text/css; charset=utf-8"
            case "json": return "application/json"
            case "png": return "image/png"
            case "svg": return "image/svg+xml"
            case "woff2": return "font/woff2"
            case "woff": return "font/woff"
            case "ttf": return "font/ttf"
            default: return "application/octet-stream"
            }
        }

        // MARK: Exportar copia: abre el menú Compartir con el archivo .json

        func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
            guard message.name == "huchaSave",
                  let body = message.body as? [String: Any],
                  let filename = body["filename"] as? String,
                  let text = body["data"] as? String else {
                return
            }
            let safeName = (filename as NSString).lastPathComponent
            let file = FileManager.default.temporaryDirectory.appendingPathComponent(safeName)
            do {
                try Data(text.utf8).write(to: file, options: .atomic)
            } catch {
                return
            }
            guard let web = webView, var top = web.window?.rootViewController else {
                return
            }
            while let presented = top.presentedViewController {
                top = presented
            }
            let share = UIActivityViewController(activityItems: [file], applicationActivities: nil)
            share.popoverPresentationController?.sourceView = web
            share.popoverPresentationController?.sourceRect = CGRect(x: web.bounds.midX, y: web.bounds.midY, width: 1, height: 1)
            top.present(share, animated: true)
        }

        // MARK: Los enlaces externos se abren en Safari

        func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            guard let url = navigationAction.request.url, let scheme = url.scheme?.lowercased() else {
                decisionHandler(.allow)
                return
            }
            if scheme == "http" || scheme == "https" || scheme == "mailto" || scheme == "tel" {
                UIApplication.shared.open(url)
                decisionHandler(.cancel)
                return
            }
            decisionHandler(.allow)
        }
    }
}
