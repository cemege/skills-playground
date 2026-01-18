# Claude Code Reference for skills-playground

This repository contains iOS development skills and reference materials for building modern iOS applications with SwiftUI, Swift Concurrency, and latest Apple technologies.

## Repository Purpose

A comprehensive skills library for iOS development workflows, designed to work like a complete iOS engineering toolkit. Each skill focuses on a specific aspect of iOS development with:
- Implementation examples
- Best practices documentation
- Common patterns and anti-patterns
- Integration guidelines

## Available Skills

### 1. ios-project-init (NEW)
**Location**: `skills/ios-project-init/SKILL.md`

**Purpose**: Create a basic iOS project with SwiftUI App lifecycle

**Use When**:
- Creating a new iOS project from scratch
- Need a clean starting point
- Want a consistent project structure

**Asks Developer For**:
- Project name and path
- Bundle identifier
- Minimum iOS version (default: 17.0)
- Swift version (default: 6.0)
- Whether to include core packages (Network, Extensions, Router)

**What It Does**:
- Creates SwiftUI App lifecycle entry point
- Sets up folder structure (App, Features, Resources, Localization)
- Optionally copies core package templates
- Initializes git repository
- Creates .gitignore for iOS/Swift

**Available Core Packages** (in `packages/`) - *Customizable Templates*:
- **Network** - Async networking (Client, Endpoint, Request/Response) → customize endpoints, auth
- **Extensions** - Swift extensions (Codable, String, Dictionary) → add your own
- **Router** - Navigation management (tabs, routes, registry) → define your app's navigation

**References**:
- `references/basic-project-structure.md` - Detailed structure documentation

---

### 2. ios-integration-setup (NEW)
**Location**: `skills/ios-integration-setup/SKILL.md`

**Purpose**: Add 3rd party integrations to an iOS project

**Use When**:
- Adding Firebase, Supabase, or other backend services
- Setting up RevenueCat for subscriptions
- Integrating analytics (Mixpanel, PostHog)
- Adding any external SDK or service

**Note**: For core packages (Network, Extensions), use `ios-project-init` instead.

**Available 3rd Party Integrations**:
- **Backend**: Firebase, Supabase
- **Monetization**: RevenueCat
- **Analytics**: Mixpanel, PostHog, Amplitude
- **Images**: Kingfisher
- **Error Tracking**: Sentry
- **Push**: OneSignal, FCM
- **Feature Flags**: LaunchDarkly

**References**:
- `references/available-packages.md` - 3rd party integration details
- `references/package-usage.md` - Usage examples for each integration

---

### 3. swift-concurrency-expert
**Location**: `skills/swift-concurrency-expert/SKILL.md`

**Purpose**: Review and fix Swift Concurrency issues in Swift 6.2+ codebases

**Use When**:
- Reviewing Swift Concurrency usage
- Improving concurrency compliance
- Fixing Swift concurrency compiler errors
- Applying actor isolation and Sendable safety

**Key Concepts**:
- Data-race safety through compile-time checks
- Approachable concurrency (single-threaded by default)
- `@MainActor` for UI-bound types
- `@concurrent` attribute for background work
- Isolated conformances for protocol safety
- Default actor isolation mode

**References**:
- `references/swift-6-2-concurrency.md` - Swift 6.2 changes and patterns
- `references/swiftui-concurrency-tour-wwdc.md` - SwiftUI-specific concurrency

---

### 4. swiftui-guidelines
**Location**: `skills/swiftui-guidelines/SKILL.md`

**Purpose**: Reference skill for SwiftUI state management, async patterns, and best practices

**Use When**:
- Implementing any SwiftUI feature
- Deciding how to manage state
- Writing async code
- Organizing view code

**Core Philosophy**:
- SwiftUI views in UIHostingController are the default UI paradigm
- Avoid legacy UIKit patterns and unnecessary abstractions
- Focus on simplicity, clarity, and native data flow
- Let SwiftUI handle the complexity

**Quick Reference**:
```swift
@State           // Local, ephemeral view state
@Binding         // Two-way data flow between views
@ObservedObject  // Shared state from ViewModel
@EnvironmentObject // App-wide singletons
```

**Async Pattern**:
```swift
// One-time load (VC lifecycle)
Task { @MainActor in await viewModel.loadData() }

// SwiftUI task when repeat is intended
.task(id: cacheKey) { await viewModel.reload() }
```

**References**:
- `references/state-management.md` - State property wrappers
- `references/async-patterns.md` - async/await patterns
- `references/composition.md` - View composition
- `references/code-organization.md` - File and code organization
- `references/best-practices.md` - Do's and don'ts

---

### 5. swiftui-liquid-glass
**Location**: `skills/swiftui-liquid-glass/SKILL.md`

**Purpose**: Implement, review, or improve SwiftUI features using iOS 26+ Liquid Glass API

**Use When**:
- Adopting Liquid Glass in new SwiftUI UI
- Refactoring existing features to Liquid Glass
- Reviewing Liquid Glass usage for correctness and performance

**Core Guidelines**:
- Prefer native Liquid Glass APIs over custom blurs
- Use `GlassEffectContainer` when multiple glass elements coexist
- Apply `.glassEffect(...)` after layout and visual modifiers
- Use `.interactive()` for elements that respond to touch/pointer
- Gate with `#available(iOS 26, *)` with fallback UI

**Quick Snippets**:
```swift
// Basic glass effect
Text("Hello")
    .padding()
    .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 16))

// Multiple glass elements
GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        Image(systemName: "scribble.variable")
            .frame(width: 72, height: 72)
            .glassEffect()
    }
}

// Glass buttons
Button("Confirm") { }
    .buttonStyle(.glassProminent)
```

**References**:
- `references/liquid-glass.md` - Complete implementation guide

---

### 6. swiftui-performance-audit
**Location**: `skills/swiftui-performance-audit/SKILL.md`

**Purpose**: Audit and improve SwiftUI runtime performance from code review and architecture

**Use When**:
- Diagnosing slow rendering or janky scrolling
- High CPU/memory usage in SwiftUI
- Excessive view updates or layout thrash
- Need guidance for Instruments profiling

**Workflow Decision Tree**:
1. **Code-First Review** - Start with code analysis
2. **Guide User to Profile** - If inconclusive, use Instruments
3. **Analyze and Diagnose** - Identify root causes
4. **Remediate** - Apply targeted fixes
5. **Verify** - Re-run captures to confirm improvements

**Common Code Smells**:
- Expensive formatters in `body`
- Computed properties doing heavy work
- Sorting/filtering in `body` or `ForEach`
- Unstable identity (`id: \.self` with non-stable values)
- Image decoding on main thread
- Broad dependencies in observable models

**Remediation Patterns**:
- Move heavy work out of `body` and cache results
- Use `@Observable` macro for granular property tracking
- Stabilize identities for `ForEach` and lists
- Downsample images before rendering
- Narrow state scope to affected views

**References**:
- `references/optimizing-swiftui-performance-instruments.md`
- `references/understanding-improving-swiftui-performance.md`
- `references/understanding-hangs-in-your-app.md`
- `references/demystify-swiftui-performance-wwdc23.md`

---

### 7. swiftui-view-refactor
**Location**: `skills/swiftui-view-refactor/SKILL.md`

**Purpose**: Refactor SwiftUI view files for consistent structure, dependency injection, and Observation usage

**Use When**:
- Cleaning up SwiftUI view layout/ordering
- Handling view models safely (non-optional when possible)
- Standardizing dependency initialization and passing

**View Ordering** (top → bottom):
1. Environment
2. `private`/`public` `let`
3. `@State` / other stored properties
4. computed `var` (non-view)
5. `init`
6. `body`
7. computed view builders / other view helpers
8. helper / async functions

**Prefer MV (Model-View) Patterns**:
- Default to MV: Views are lightweight state expressions
- Favor `@State`, `@Environment`, `@Query`, `task`/`onChange`
- Inject services via `@Environment`
- Split large views into subviews rather than introducing ViewModels
- Only use ViewModels when clearly necessary

**View Model Handling** (if already present):
- Make it non-optional when possible
- Pass dependencies via `init`, then into view model
- Avoid `bootstrapIfNeeded` patterns

**Example**:
```swift
@State private var viewModel: SomeViewModel

init(dependency: Dependency) {
    _viewModel = State(initialValue: SomeViewModel(dependency: dependency))
}
```

**References**:
- `references/mv-patterns.md` - MV-first guidance and rationale

---

## Key Philosophical Principles

### Modern SwiftUI (2025)
- **Views are pure state expressions** - No unnecessary ViewModels
- **Services in environment, logic in services/models** - Not in views
- **Trust the framework** - Use `@State`, `@Environment`, `@Observable`
- **Test business logic, not views** - Keep views simple and declarative
- **Composition over ViewModels** - Split large views into smaller views

### Swift Concurrency (6.2)
- **Single-threaded by default** - Main actor isolation
- **Explicit concurrency** - Use `@concurrent` when needed
- **Data-race safety at compile time** - No runtime surprises
- **Isolated conformances** - Protocol conformances can be actor-isolated

### Performance Mindset
- **Profile early and often** - Use Instruments during development
- **Keep work out of view bodies** - Precompute, cache, async load
- **Narrow dependencies** - Reduce update fan-out
- **Stable identities** - Critical for lists and animations

### Code Organization
- **Feature-based structure** - Not type-based (Views/, ViewModels/)
- **MARK comments** - Separate logical sections
- **Small, focused files** - Extract when growing too large
- **Avoid AnyView** - Use `@ViewBuilder` and generics

---

## How to Use These Skills

When working on iOS development tasks in this repository:

1. **Creating a new project** → Use `ios-project-init` for minimal setup
2. **Adding integrations** → Use `ios-integration-setup` to add packages
3. **Starting new SwiftUI features** → Reference `swiftui-guidelines`
4. **Implementing Liquid Glass effects** → Use `swiftui-liquid-glass`
5. **Fixing concurrency errors** → Apply `swift-concurrency-expert`
6. **Performance issues** → Follow `swiftui-performance-audit` workflow
7. **Refactoring views** → Use `swiftui-view-refactor` ordering and patterns

### Project Creation Workflow

```
ios-project-init → ios-integration-setup → Start building features
```

1. Create empty project with `ios-project-init`
2. Add needed packages with `ios-integration-setup`
3. Build features using development skills (swiftui-guidelines, etc.)

---

## Quick Decision Trees

### Should I create a ViewModel?
- Is this just local UI state? → Use `@State`
- Is this shared between views? → Use `@Environment` with a service
- Does this need complex business logic? → Maybe, but prefer MV pattern first
- Legacy code already has ViewModels? → Keep pattern consistent, make non-optional

### How should I handle async work?
- One-time load in VC lifecycle? → `Task` in `viewDidLoad`
- Reload when view appears? → `.task` with guard
- Reload when value changes? → `.task(id: value)`
- Always use `@MainActor` for UI updates

### Is my view too complex?
- Body > 1 screen of code? → Extract subviews
- Multiple logical sections? → Use computed view properties
- Reusable component? → Create separate View struct
- Complex state logic? → Consider extracting to a service

---

## Modern Swift Features to Use

- `async/await` over Combine
- Swift Concurrency (actors, `@MainActor`)
- `@Observable` for granular property tracking
- Value types (structs) by default
- `@ViewBuilder` for conditional content
- Swift 6 data-race safety when available

---

## What to Avoid

- Unnecessary ViewModels for simple views
- `AnyView` (use `@ViewBuilder` or generics)
- Combine for simple async operations
- Over-abstraction without clear benefit
- Fighting SwiftUI's update mechanism
- Heavy work in view `body` computations
- Broad dependencies causing update storms
- Legacy UIKit patterns in SwiftUI code

---

## Repository Structure

```
skills-playground/
├── skills/
│   ├── ios-project-init/           # Project creation
│   │   ├── SKILL.md
│   │   └── references/
│   ├── ios-integration-setup/      # Package integration
│   │   ├── SKILL.md
│   │   └── references/
│   ├── swift-concurrency-expert/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── swiftui-guidelines/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── swiftui-liquid-glass/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── swiftui-performance-audit/
│   │   ├── SKILL.md
│   │   └── references/
│   └── swiftui-view-refactor/
│       ├── SKILL.md
│       └── references/
├── packages/                       # Core package templates (customizable)
│   ├── Network/                    # Async networking layer
│   ├── Extensions/                 # Common Swift extensions
│   └── Router/                     # Navigation management
├── examples/                       # Example projects (future)
└── docs/                          # Additional documentation
```

---

## Attribution

Skills structure and several skill definitions copied from @Dimillian's `Dimillian/Skills` repository (2025-12-31). Adapted and extended for this project's needs.

---

## For Claude Code: Session Initialization

When starting a new session in this repository:

1. Read this CLAUDE.md file first
2. Reference specific skill SKILL.md files for detailed workflows
3. Check reference materials in `skills/*/references/` for technical details
4. Apply the philosophical principles consistently across all work
5. Use the decision trees to guide architectural choices

The goal is to produce iOS code that is:
- Modern and idiomatic Swift/SwiftUI
- Performant and data-race safe
- Simple and maintainable
- Aligned with Apple's latest guidance and APIs
