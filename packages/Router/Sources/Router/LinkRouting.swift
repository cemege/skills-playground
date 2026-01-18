//
//  LinkRouting.swift
//  Router
//

import SwiftUI

/// A lightweight contract for URL routing.
///
/// Keep URL parsing/decision logic in a router object (not scattered across views),
/// and attach it at the root with `withLinkRouter(_:)`.
@MainActor
public protocol LinkRouting: AnyObject {
    func handle(url: URL) -> OpenURLAction.Result
    func handleDeepLink(url: URL) -> OpenURLAction.Result
}

public extension View {
    /// Wires a link router into SwiftUI's `openURL` environment and `.onOpenURL`.
    func withLinkRouter(_ router: any LinkRouting) -> some View {
        self
            .environment(
                \.openURL,
                OpenURLAction { url in
                    router.handle(url: url)
                }
            )
            .onOpenURL { url in
                _ = router.handleDeepLink(url: url)
            }
    }
}
