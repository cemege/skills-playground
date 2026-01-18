//
//  TabRouter.swift
//  Router
//
//  Provides per-tab `RouterPath` instances and bindings.
//

import SwiftUI

/// Manages a set of routers for a tabbed app so each tab can have an independent navigation history.
///
/// Note: This type is intentionally *not* `@Observable` to avoid nesting observable objects.
/// Views should observe the per-tab `RouterPath` instances instead (those are `@Observable`).
@MainActor
public final class TabRouter<Tab: Hashable, Route: Hashable, Sheet: Identifiable> {
    private var routers: [Tab: RouterPath<Route, Sheet>] = [:]

    public init() {}

    public func router(for tab: Tab) -> RouterPath<Route, Sheet> {
        if let router = routers[tab] { return router }
        let router = RouterPath<Route, Sheet>()
        routers[tab] = router
        return router
    }

    /// A binding suitable for `NavigationStack(path:)`.
    public func binding(for tab: Tab) -> Binding<[Route]> {
        let router = router(for: tab)
        return Binding(
            get: { router.path },
            set: { router.path = $0 }
        )
    }
}
