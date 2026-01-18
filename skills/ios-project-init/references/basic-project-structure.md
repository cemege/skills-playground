# Basic iOS Project Structure

This document details the minimal project structure created by `ios-project-init`.

## Directory Layout

```
ProjectName/
├── ProjectName/                    # Main app target
│   ├── App/                        # App lifecycle
│   │   └── ProjectNameApp.swift    # @main entry point
│   ├── Features/                   # Feature modules
│   │   └── .gitkeep                # Placeholder
│   ├── Resources/                  # Assets and resources
│   │   ├── Assets.xcassets/        # Image and color assets
│   │   │   ├── AccentColor.colorset/
│   │   │   ├── AppIcon.appiconset/
│   │   │   └── Contents.json
│   └── Localization/
│       └── Localizable.xcstrings   # String catalog for localization
│   └── Info.plist                  # App configuration
├── ProjectName.xcodeproj/          # Xcode project bundle
├── Packages/                       # Local Swift packages (added later)
├── .gitignore                      # iOS/Swift gitignore
└── README.md                       # Project documentation
```

## File Templates

### ProjectNameApp.swift

```swift
import SwiftUI

@main
struct ProjectNameApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### ContentView.swift

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

### Info.plist

Minimal Info.plist with:
- Bundle display name
- Bundle identifier
- Required device capabilities
- Supported interface orientations

### .gitignore

Standard iOS/Swift gitignore covering:
- Xcode user data
- Build products
- CocoaPods (if used)
- Swift Package Manager
- Environment files
- OS-specific files

```gitignore
# Xcode
*.xcodeproj/*
!*.xcodeproj/project.pbxproj
!*.xcodeproj/xcshareddata/
*.xcuserstate
*.xcuserdatad/
*.xcworkspace/*
!*.xcworkspace/contents.xcworkspacedata
!*.xcworkspace/xcshareddata/

# Build
build/
DerivedData/
*.ipa
*.dSYM.zip
*.dSYM

# Swift Package Manager
.build/
.swiftpm/
Package.resolved

# CocoaPods
Pods/

# Environment
.env
.env.*
*.xcconfig

# OS
.DS_Store
Thumbs.db
```

## Feature Directory Organization

The `Features/` directory follows a feature-based structure:

```
Features/
├── Home/
│   ├── HomeView.swift
│   ├── HomeViewModel.swift (if needed)
│   └── Components/
├── Settings/
│   ├── SettingsView.swift
│   └── Components/
└── Shared/
    └── Components/
```

**Guidelines:**
- Group by feature, not by type
- Keep related files together
- Use `Shared/` for truly shared components
- Prefer composition over deep hierarchies

## Core Packages (Customizable Templates)

When creating a project, you can include these base packages from `skills-playground/packages/`:

```
Packages/
├── Network/      # Async networking layer
├── Extensions/   # Common Swift extensions
└── Router/       # Navigation management
```

**Important:** These are **templates**, not final solutions. You should customize them:

| Package | What to Customize |
|---------|-------------------|
| Network | Your API domains, endpoints, auth logic, error types |
| Extensions | Add project-specific extensions as needed |
| Router | Your app's tabs (`AppTab`), routes, navigation flows |

Each package is a local Swift package added to the Xcode project.

## Adding 3rd Party Integrations

For external services (Firebase, Supabase, RevenueCat, etc.), use `ios-integration-setup` after project creation.

## Xcode Project Settings

### Build Settings (Defaults)
- **iOS Deployment Target**: 17.0
- **Swift Language Version**: 6.0
- **Swift Strict Concurrency**: Complete
- **Enable Bitcode**: No (deprecated)

### Capabilities (Add as needed)
- Push Notifications
- Sign in with Apple
- In-App Purchase
- HealthKit
- etc.

## Why This Structure?

1. **Minimal** - Only essential files, nothing extra
2. **Scalable** - Features directory grows naturally
3. **Modern** - SwiftUI-first, Swift 6 ready
4. **Flexible** - Add packages and integrations as needed
5. **Clean** - Clear separation of concerns

## Common Modifications

### Adding a Tab-based App

Replace ContentView with:
```swift
struct ContentView: View {
    var body: some View {
        TabView {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }

            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
        }
    }
}
```

### Adding Environment Objects

Update App entry:
```swift
@main
struct ProjectNameApp: App {
    @State private var authService = AuthService()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(authService)
        }
    }
}
```

### Adding App Delegate (if needed)

```swift
@main
struct ProjectNameApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        // Setup code
        return true
    }
}
```
