---
name: swiftui-guidelines
description: Reference skill for SwiftUI state management, async patterns, and best practices. Use when implementing SwiftUI views and features.
type: reference
---

# SwiftUI Guidelines Reference

Best practices and patterns for SwiftUI development in this project.

## Quick Navigation

| Need to... | Read |
|------------|------|
| Manage state (@State, @Binding, etc.) | [state-management.md](references/state-management.md) |
| Handle async operations, API calls | [async-patterns.md](references/async-patterns.md) |
| Compose views, avoid AnyView | [composition.md](references/composition.md) |
| Organize code, use MARK comments | [code-organization.md](references/code-organization.md) |
| Know what to do and avoid | [best-practices.md](references/best-practices.md) |

## Core Philosophy

- **SwiftUI views in UIHostingController** are the default UI paradigm
- **Avoid legacy UIKit patterns** and unnecessary abstractions
- **Focus on simplicity, clarity, and native data flow**
- **Let SwiftUI handle the complexity** - don't fight the framework

## Quick Reference

### State Management
```swift
@State           // Local, ephemeral view state
@Binding         // Two-way data flow between views
@ObservedObject  // Shared state from ViewModel
@EnvironmentObject // App-wide singletons
```

### Async Pattern
```swift
// One-time load (VC lifecycle)
Task { @MainActor in await viewModel.loadData() }

// SwiftUI task when repeat is intended
.task(id: cacheKey) { await viewModel.reload() }
```

### Modern Swift
- Use `async/await` over Combine
- Use Swift Concurrency (actors)
- Use `@MainActor` for UI updates

## When to Use This Skill

Reference this skill when:
- Implementing any SwiftUI feature
- Deciding how to manage state
- Writing async code
- Organizing view code
