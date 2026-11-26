import SwiftUI

/// Hucha para iPhone: la misma app que la versión web y la de Android,
/// incluida dentro de la app (carpeta Web) y mostrada en un WKWebView.
@main
struct HuchaApp: App {
    var body: some Scene {
        WindowGroup {
            WebAppView()
                .ignoresSafeArea()
                .background(Color("Papel").ignoresSafeArea())
        }
    }
}
