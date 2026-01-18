---
name: ios-project-init
description: Create a basic iOS project with SwiftUI App lifecycle. Asks for path, iOS/Swift versions, and optional core packages.
type: workflow
---

# iOS Project Initialization

Create minimal, clean iOS projects ready for development.

## Core Philosophy

- **Start minimal** - Only essential files and optional core packages
- **Developer choice** - Ask what they need, don't assume
- **Customizable templates** - Core packages are starting points, not final solutions
- **Modern defaults** - SwiftUI App lifecycle, latest Swift

## When to Use This Skill

Use this skill when:
- Creating a new iOS project from scratch
- Need a clean starting point
- Want a consistent project structure

## Workflow

### Step 1: Ask Project Configuration

Ask the developer these questions:

| Question | Example | Default |
|----------|---------|---------|
| **Project name** | "MyApp" | Required |
| **Project path** | "~/Developer/projects" | Required |
| **Bundle identifier** | "com.company.myapp" | Required |
| **Minimum iOS version** | 17.0, 18.0 | 17.0 |
| **Swift version** | 5.9, 6.0 | 6.0 |

### Step 2: Ask About Core Packages

Ask if developer wants to include available packages:

> **Note:** These packages are **base templates** designed to be customized for your project. They provide a starting structure that you should modify to fit your specific needs.

**Available Packages** (from `packages/` directory):

- [ ] **Network** - Lightweight async networking layer
  - Client, Endpoint, Request/Response protocols
  - HTTPMethod, NetworkError handling
  - SwiftUI environment key integration
  - **Customize:** Add your API endpoints, auth logic, error types

- [ ] **Extensions** - Common Swift extensions
  - Codable helpers (Decodable, Encodable)
  - Dictionary utilities
  - String extensions
  - Closure type aliases
  - **Customize:** Add project-specific extensions as needed

- [ ] **Router** - Navigation management for SwiftUI
  - Tab-based navigation with NavigationStack
  - RouteProtocol for type-safe destinations
  - RouteRegistry for cross-feature navigation
  - **Customize:** Define your app's tabs, routes, and navigation flows

### Step 3: Create Project Structure

```
{ProjectPath}/{ProjectName}/
├── {ProjectName}/
│   ├── App/
│   │   └── {ProjectName}App.swift    # @main entry point
│   ├── Features/                      # Feature modules go here
│   ├── Resources/
│   │   └── Assets.xcassets/           # Asset catalog
│   ├── Localization/
│   │   └── Localizable.xcstrings      # String catalog
│   └── Info.plist                     # App configuration
├── Packages/                          # Local packages (if selected)
│   ├── Network/                       # (customizable template)
│   ├── Extensions/                    # (customizable template)
│   └── Router/                        # (customizable template)
├── {ProjectName}.xcodeproj/           # Xcode project
├── .gitignore                         # iOS/Swift gitignore
└── README.md                          # Basic readme
```

### Step 4: Generate Core Files

#### SwiftUI App Entry Point
```swift
import SwiftUI

@main
struct {ProjectName}App: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

#### Initial ContentView
```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Hello, World!")
    }
}

#Preview {
    ContentView()
}
```

### Step 5: Copy Selected Packages

If packages were selected:
1. Copy from `skills-playground/packages/` to project's `Packages/` directory
2. Add as local Swift package dependencies in Xcode project
3. **Remind developer:** These are templates to customize!

### Step 6: Initialize Git

```bash
cd {ProjectPath}/{ProjectName}
git init
git add .
git commit -m "Initial project setup"
```

## Package Customization Guide

### Network Package - What to Customize

The Network package provides a base async networking layer. Customize:

```swift
// 1. Add your API domains
enum Domain: String {
    case production = "api.yourapp.com"
    case staging = "staging-api.yourapp.com"
}

// 2. Define your endpoints
enum UserEndpoint: Endpoint {
    case getProfile
    case updateProfile(data: ProfileUpdateRequest)

    var path: String { ... }
    var method: HTTPMethod { ... }
}

// 3. Add authentication handling
// Modify Client to include your auth token logic

// 4. Add custom error types
enum AppNetworkError: Error {
    case unauthorized
    case serverMaintenance
    // Your app-specific errors
}
```

### Extensions Package - What to Customize

Add extensions specific to your project:

```swift
// Add domain-specific extensions
extension Color {
    static let appPrimary = Color("AppPrimary")
    static let appSecondary = Color("AppSecondary")
}

extension String {
    var isValidUsername: Bool { ... }
}

// Add model-specific helpers
extension User {
    var displayName: String { ... }
}
```

### Router Package - What to Customize

The Router package needs to match your app's navigation:

```swift
// 1. Define YOUR app's tabs
public enum AppTab: String, CaseIterable, Identifiable, Hashable, Sendable {
    case home, discover, settings  // Change to your tabs

    public var id: String { rawValue }

    public var icon: String {
        switch self {
        case .home: return "house"
        case .discover: return "safari"
        case .settings: return "gear"
        }
    }
}

// 2. Define routes for each feature
enum HomeRoutes: RouteProtocol {
    case detail(id: String)
    case settings

    @MainActor @ViewBuilder
    func view() -> AnyView {
        switch self {
        case .detail(let id):
            AnyView(DetailView(id: id))
        case .settings:
            AnyView(SettingsView())
        }
    }
}

// 3. Register routes at app startup
RouteRegistry.shared.register(id: "home.detail") { param in
    HomeRoutes.detail(id: param as? String ?? "")
}
```

## Example Conversation

**Claude:** I'll help you create a new iOS project. I need some information:

1. What's the project name?
2. Where should I create it? (full path)
3. What's the bundle identifier?
4. Minimum iOS version? (default: 17.0)
5. Swift version? (default: 6.0)

**Developer:**
- Name: WeatherApp
- Path: ~/Developer/apps
- Bundle ID: com.mycompany.weatherapp
- iOS 18.0
- Swift 6.0

**Claude:** Do you want to include any core packages? These are base templates you'll customize for your project:

- [ ] Network - Async networking (customize: endpoints, auth, errors)
- [ ] Extensions - Swift helpers (customize: add your own)
- [ ] Router - Navigation (customize: tabs, routes)

**Developer:** Yes, all three.

**Claude:** Creating WeatherApp at ~/Developer/apps with iOS 18.0, Swift 6.0, and including Network, Extensions, and Router packages.

**Important:** These packages are templates! You should customize:
- **Network:** Add your weather API endpoints and auth
- **Router:** Change AppTab to your tabs (e.g., weather, favorites, settings)
- **Extensions:** Add weather-specific helpers as needed

## Project Configuration

Settings are based on developer input:

| Setting | Value |
|---------|-------|
| iOS Deployment Target | Developer specified |
| Swift Language Version | Developer specified |
| App Lifecycle | SwiftUI App |
| UI Framework | SwiftUI |
| Device Support | iPhone & iPad |

## Package Source

Packages are copied from this repository:
```
skills-playground/packages/
├── Network/          # Async networking template
├── Extensions/       # Swift extensions template
└── Router/           # Navigation template
```

**These are starting points, not final solutions.** Customize them for your project's specific needs.

## References

- [Basic Project Structure](references/basic-project-structure.md) - Detailed structure documentation

## Next Steps After Creation

1. Open project in Xcode
2. **Customize the packages** for your project needs
3. Build to verify setup
4. Run `ios-integration-setup` for 3rd party integrations (Firebase, etc.)
5. Start building features using `swiftui-guidelines`
