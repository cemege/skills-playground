//
//  RouterPath.swift
//  Router
//
//  A lightweight, SwiftUI-native navigation state container.
//

import Foundation
import Observation

/// Holds navigation stack state and sheet presentation state.
///
/// This aligns with the "one NavigationStack per tab" approach:
/// - Each tab owns a `RouterPath`
/// - Views read the router from the environment to navigate/present sheets
///
/// Route mapping is expected to be handled by the app via `navigationDestination(for:)`.
@MainActor
@Observable
public final class RouterPath<Route: Hashable, Sheet: Identifiable> {
    public var path: [Route] = []
    public var presentedSheet: Sheet?

    public init() {}

    public func navigate(to route: Route) {
        path.append(route)
    }

    public func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    public func popToRoot() {
        path.removeAll()
    }

    public func reset() {
        popToRoot()
        presentedSheet = nil
    }

    public func present(sheet: Sheet) {
        presentedSheet = sheet
    }

    public func dismissSheet() {
        presentedSheet = nil
    }
}
