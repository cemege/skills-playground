//
//  Router.swift
//  Router
//
//  Created by Cem Ege on 22.11.2024.
//

import SwiftUI

// MARK: - App Tab Types (template)

/// Represents the main tabs in the application.
///
/// This is a template type intended to be customized per-app.
public enum AppTab: String, CaseIterable, Identifiable, Hashable, Sendable {
    case home, search, profile
    
    /// Unique identifier for the tab, uses the raw string value.
    public var id: String { rawValue }
    
    /// System icon name for the tab.
    public var icon: String {
        switch self {
        case .home: return "house"
        case .search: return "magnifyingglass"
        case .profile: return "person"
        }
    }
}

/// Environment value extension to access the current tab from any view.
extension EnvironmentValues {
    @Entry public var currentTab: AppTab = .home
}
