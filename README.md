# iOS Skills Playground

A comprehensive collection of iOS development skills and workflows for **Claude Code**, designed to streamline iOS application development using modern technologies and best practices.

## Ultimate Goal: Automated iOS App Factory

**The vision:** A developer describes what they want → AI uses these skills and templates → out comes a production-ready iOS app.

This repository is an **automated iOS app factory**. The end goal is fully automated iOS app generation:

1. Developer says "I want a weather app with subscriptions"
2. AI uses `ios-project-init` → scaffolds the project structure
3. AI uses `ios-integration-setup` → adds RevenueCat, Firebase, etc.
4. AI follows `swiftui-guidelines` → builds features correctly
5. AI applies `swift-concurrency-expert` → ensures data-race safety
6. **Result:** Working iOS app following modern best practices

The skills are the "recipes" and packages are the "ingredients" - together they enable AI to produce consistent, high-quality iOS apps without the developer needing to know every implementation detail.

## What This Repository Does

This repository provides **skills** (instruction sets) that guide Claude Code through iOS development tasks. Think of it as a complete iOS engineering toolkit that Claude can reference when helping you build apps.

### Key Features

- **Project Initialization** - Create new iOS projects with consistent structure
- **Package Templates** - Customizable base packages (Network, Extensions, Router)
- **3rd Party Integrations** - Firebase, Supabase, RevenueCat, analytics, and more
- **Development Guidelines** - SwiftUI best practices, concurrency patterns, performance optimization
- **Code Quality** - View refactoring, architecture patterns, Liquid Glass UI

## Repository Structure

```
skills-playground/
├── skills/                           # Claude Code skill definitions
│   ├── app-store-changelog/          # App Store release notes from git
│   ├── gh-issue-fix-flow/            # GitHub issue → fix → test → ship
│   ├── ios-debugger-agent/           # Build/run/debug on simulator
│   ├── ios-project-init/             # Create new iOS projects
│   ├── ios-integration-setup/        # Add 3rd party integrations
│   ├── swift-concurrency-expert/     # Swift 6.2+ concurrency
│   ├── swiftui-guidelines/           # SwiftUI best practices
│   ├── swiftui-liquid-glass/         # iOS 26+ Liquid Glass API
│   ├── swiftui-performance-audit/    # Performance optimization
│   ├── swiftui-ui-patterns/          # SwiftUI UI patterns & components
│   └── swiftui-view-refactor/        # View structure patterns
├── packages/                         # Customizable package templates
│   ├── Network/                      # Async networking layer
│   ├── Extensions/                   # Common Swift extensions
│   └── Router/                       # Navigation management
├── CLAUDE.md                         # Main instructions for Claude Code
└── README.md                         # This file
```

## Available Skills

### Project Setup Skills

#### 1. ios-project-init
Create a new iOS project from scratch.

**Asks for:**
- Project name and path
- Bundle identifier
- Minimum iOS version
- Swift version
- Core packages to include

**Creates:**
- SwiftUI App lifecycle entry point
- Folder structure (App, Features, Resources, Localization)
- Git repository with .gitignore
- Optional: Network, Extensions, Router packages

#### 2. ios-integration-setup
Add 3rd party integrations to your project.

**Available Integrations:**
| Category | Services |
|----------|----------|
| Backend | Firebase, Supabase |
| Monetization | RevenueCat |
| Analytics | Mixpanel, PostHog, Amplitude |
| Images | Kingfisher |
| Error Tracking | Sentry |
| Push Notifications | OneSignal, FCM |
| Feature Flags | LaunchDarkly |

### Development Skills

#### 3. swift-concurrency-expert
Review and fix Swift Concurrency issues in Swift 6.2+ codebases.

- Data-race safety through compile-time checks
- `@MainActor` for UI-bound types
- `@concurrent` attribute for background work
- Isolated conformances for protocol safety

#### 4. swiftui-guidelines
Reference for SwiftUI state management, async patterns, and best practices.

- State property wrappers (`@State`, `@Binding`, `@Observable`)
- Async patterns with `.task` and `async/await`
- View composition and organization
- MV (Model-View) patterns over MVVM

#### 5. swiftui-liquid-glass
Implement iOS 26+ Liquid Glass API effects.

- `.glassEffect()` modifier usage
- `GlassEffectContainer` for multiple elements
- Glass button styles
- Availability checks and fallbacks

#### 6. swiftui-performance-audit
Diagnose and fix SwiftUI performance issues.

- Code-first review for common smells
- Instruments profiling guidance
- Remediation patterns
- Identity stability for lists

#### 7. swiftui-view-refactor
Refactor views for consistent structure and patterns.

- Standard property ordering
- Dependency injection patterns
- MV-first approach
- View model handling (when necessary)

#### 8. swiftui-ui-patterns
Best practices and example-driven guidance for building SwiftUI views and components.

- Component references for `TabView`, `NavigationStack`, sheets, lists, grids, and more
- Scaffolding guidance for app wiring and dependency graph

#### 9. app-store-changelog
Generate user-facing App Store release notes from git history.

- Collect commits and touched files since last tag (or a specified ref)
- Convert changes into benefit-focused “What’s New” bullets

#### 10. ios-debugger-agent
Build, run, and debug iOS projects on simulators (tooling-driven workflow).

- Simulator discovery + scheme setup
- UI inspection, taps/typing/gestures, screenshots, and logs

#### 11. gh-issue-fix-flow
Resolve GitHub issues end-to-end using `gh`, local edits, builds/tests, and git.

- Fetch issue context
- Implement minimal fix + validate
- Commit/push with closing message

## Core Package Templates

These packages are **customizable starting points**, not final solutions. Modify them for your project's needs.

### Network
Lightweight async networking layer.

```swift
// Customize: Add your endpoints
enum UserEndpoint: Endpoint {
    case getProfile
    case updateProfile(data: ProfileUpdateRequest)
}
```

**Contains:** Client, Endpoint protocol, Request/Response, HTTPMethod, NetworkError, SwiftUI environment key

### Extensions
Common Swift extensions.

```swift
// Customize: Add project-specific extensions
extension Color {
    static let appPrimary = Color("AppPrimary")
}
```

**Contains:** Codable helpers, Dictionary utilities, String extensions, Closure type aliases

### Router
Navigation management for SwiftUI.

```swift
// Customize: Define your app's tabs
public enum AppTab: String, CaseIterable {
    case home, discover, settings  // Your tabs here
}
```

**Contains:** Router class, RouteProtocol, RouteRegistry, AppTab enum, environment values

## Workflow

### Creating a New Project

```
1. Run ios-project-init
   ↓
2. Provide: name, path, bundle ID, iOS version, Swift version
   ↓
3. Select core packages: Network, Extensions, Router
   ↓
4. Customize packages for your project
   ↓
5. Run ios-integration-setup for 3rd party services
   ↓
6. Start building features
```

### Development Flow

```
Building Features    → swiftui-guidelines
Concurrency Issues   → swift-concurrency-expert
Performance Problems → swiftui-performance-audit
Refactoring Views    → swiftui-view-refactor
UI Patterns          → swiftui-ui-patterns
iOS 26+ Glass UI     → swiftui-liquid-glass
Release Notes        → app-store-changelog
Debugging            → ios-debugger-agent
Issue Fixes          → gh-issue-fix-flow
```

## How Claude Code Uses This

When you work with Claude Code in this repository:

1. **CLAUDE.md** is read automatically, providing context about available skills
2. **Skill files** (SKILL.md) contain detailed workflows and instructions
3. **Reference files** provide technical documentation and examples
4. **Package templates** are copied to new projects when requested

### Example Interaction

```
You: Create a new iOS app called WeatherApp

Claude: I'll use the ios-project-init skill. I need some information:
- Where should I create it?
- What's the bundle identifier?
- Minimum iOS version?
- Do you want to include Network, Extensions, or Router packages?

You: ~/Developer/apps, com.mycompany.weather, iOS 18, include all packages

Claude: Creating project with Network, Extensions, and Router...
Remember to customize:
- Network: Add your weather API endpoints
- Router: Change AppTab to your tabs (weather, favorites, settings)
- Extensions: Add weather-specific helpers
```

## Technologies

- **Swift 6.0+** - Latest language features and concurrency
- **SwiftUI** - Declarative UI framework
- **iOS 17.0+** - Minimum deployment target (configurable)
- **Swift Package Manager** - Dependency management
- **Xcode 16+** - Development environment

## Philosophy

### Modern SwiftUI (2025)
- Views are pure state expressions
- Services in environment, logic in services/models
- Trust the framework (`@State`, `@Environment`, `@Observable`)
- Composition over ViewModels

### Swift Concurrency (6.2)
- Single-threaded by default (main actor)
- Explicit concurrency with `@concurrent`
- Data-race safety at compile time

### Performance Mindset
- Profile early and often
- Keep work out of view bodies
- Narrow dependencies, stable identities

## Resources

- [Dimillian/Skills](https://github.com/Dimillian/Skills) — upstream skill library we’ve imported/adapted from for this factory.

## Attribution

Skills structure and several skill definitions adapted from [@Dimillian's Skills repository](https://github.com/Dimillian/Skills) (2025-12-31).
Additional skills imported and adapted from [Skills Public](https://github.com/Dimillian/Skills) (MIT licensed, 2026).

## License

MIT
