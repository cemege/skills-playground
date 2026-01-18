//
//  View+Sheets.swift
//  Router
//

import SwiftUI

public extension View {
    /// A tiny helper to keep sheet routing centralized and enum-driven (via `Identifiable` sheets).
    ///
    /// This matches the recommended `.sheet(item:)` approach and keeps the "mapping switch"
    /// in one place at the app/root level.
    func withSheetDestinations<Sheet: Identifiable, Content: View>(
        sheet: Binding<Sheet?>,
        @ViewBuilder content: @escaping (Sheet) -> Content
    ) -> some View {
        self.sheet(item: sheet, content: content)
    }
}
