# Best Practices

## DO

### Write Self-Contained Views
```swift
// Good - view owns its state
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        Button("Count: \(count)") {
            count += 1
        }
    }
}
```

### Use Property Wrappers as Intended
```swift
@State           // Local view state
@Binding         // Parent-child data flow
@ObservedObject  // External observable
@EnvironmentObject // Shared singletons
```

### Use Swift's Type System
```swift
// Good - type-safe enums
enum LoadingState {
    case idle
    case loading
    case loaded(Data)
    case failed(Error)
}

@Published var state: LoadingState = .idle
```

### Break Strong Reference Cycles
```swift
// In closures
viewModel.onComplete = { [weak self] result in
    self?.handleResult(result)
}
```

### Use Guard for Early Exit
```swift
func processUser(_ user: User?) {
    guard let user = user else { return }
    // Continue with valid user
}
```

### Meet App Store Guidelines
- No private APIs
- Proper permission usage
- Privacy compliance

---

## DON'T

### Create ViewModels for Every View
```swift
// Bad - overkill for simple view
struct SimpleTextViewModel: ObservableObject {
    @Published var text = "Hello"
}

// Good - just use @State
struct SimpleTextView: View {
    @State private var text = "Hello"
}
```

### Move State Out Unnecessarily
```swift
// Bad - state should stay in view
class ToggleManager: ObservableObject {
    @Published var isOn = false
}

// Good - simple local state
@State private var isOn = false
```

### Add Abstraction Without Benefit
```swift
// Bad - unnecessary protocol for simple service
protocol TextFormatterProtocol {
    func format(_ text: String) -> String
}

class TextFormatter: TextFormatterProtocol {
    func format(_ text: String) -> String {
        text.capitalized
    }
}

// Good - just use the method
func format(_ text: String) -> String {
    text.capitalized
}
```

### Use Combine for Simple Async
```swift
// Bad - overcomplicated
publisher
    .receive(on: DispatchQueue.main)
    .sink { ... }
    .store(in: &cancellables)

// Good - simple and clear
await fetchData()
```

### Fight SwiftUI's Update Mechanism
```swift
// Bad - forcing updates
@State private var forceUpdate = UUID()

Button("Refresh") {
    forceUpdate = UUID()  // Hack!
}

// Good - let SwiftUI manage updates
@Published var data: [Item] = []
```

### Overcomplicate Simple Features
```swift
// Bad - too much abstraction
protocol FeatureToggleProtocol { }
class FeatureToggleManager: FeatureToggleProtocol { }
struct FeatureToggleView<Manager: FeatureToggleProtocol>: View { }

// Good - just build it
struct SettingsView: View {
    @State private var notificationsEnabled = true

    var body: some View {
        Toggle("Notifications", isOn: $notificationsEnabled)
    }
}
```

---

## Modern Swift Features

### Use Swift Concurrency
```swift
func loadData() async throws -> Data {
    try await apiClient.fetch()
}
```

### Use Actors for Shared State
```swift
actor DataCache {
    private var cache: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        cache[key]
    }

    func set(_ key: String, data: Data) {
        cache[key] = data
    }
}
```

### Leverage Swift 6 Data Race Safety
When available, enable strict concurrency checking.

### Embrace Value Types
```swift
// Good - value type
struct UserProfile {
    var name: String
    var email: String
}

// Use reference types only when needed
class UserSession: ObservableObject {
    @Published var isLoggedIn = false
}
```

---

## Summary

Write SwiftUI code that looks and feels like SwiftUI. The framework has matured - trust its patterns. Focus on solving user problems, not implementing architectural patterns from other platforms.
