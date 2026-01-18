# State Management

Use SwiftUI's built-in property wrappers appropriately.

## Property Wrappers

| Wrapper | Use For |
|---------|---------|
| `@State` | Local, ephemeral view state |
| `@Binding` | Two-way data flow between views |
| `@ObservedObject` | Shared state from ViewModel (pre-iOS 17) |
| `@EnvironmentObject` | App-wide singletons |
| `@FocusState` | Keyboard focus management |

## State Ownership Principles

1. **Views own their local state** unless sharing is required
2. **State flows down, actions flow up**
3. **Keep state as close to where it's used as possible**
4. **Extract shared state only when multiple views need it**

## @State - Local State

For simple, view-local state:

```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") {
                count += 1
            }
        }
    }
}
```

## @Binding - Child-Parent Communication

Pass state to child views:

```swift
struct ParentView: View {
    @State private var isOn = false

    var body: some View {
        ToggleChildView(isOn: $isOn)
    }
}

struct ToggleChildView: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("Enable", isOn: $isOn)
    }
}
```

## @ObservedObject - ViewModel State

Connect to ViewModels:

```swift
struct ProfileView: View {
    @ObservedObject var viewModel: ProfileViewModel

    var body: some View {
        Group {
            if let profile = viewModel.profile {
                ProfileContent(profile: profile)
            } else {
                EmptyView()
            }
        }
    }
}
```

Trigger the initial load from the hosting VC (viewDidLoad) or a guarded `.task` when appropriate. Loading HUDs are handled via `viewControllerProvider` in the ViewModel.

## @EnvironmentObject - Shared Singletons

For app-wide state (use sparingly):

```swift
struct AppRoot: View {
    @StateObject private var session = SessionManager()

    var body: some View {
        ContentView()
            .environmentObject(session)
    }
}

struct SomeDeepView: View {
    @EnvironmentObject var session: SessionManager

    var body: some View {
        Text("Welcome, \(session.user?.name ?? "Guest")")
    }
}
```

## @FocusState - Keyboard Management

```swift
struct LoginForm: View {
    @State private var email = ""
    @State private var password = ""
    @FocusState private var focusedField: Field?

    enum Field {
        case email, password
    }

    var body: some View {
        VStack {
            TextField("Email", text: $email)
                .focused($focusedField, equals: .email)

            SecureField("Password", text: $password)
                .focused($focusedField, equals: .password)
        }
        .onSubmit {
            switch focusedField {
            case .email:
                focusedField = .password
            default:
                focusedField = nil
            }
        }
    }
}
```

## Anti-Patterns

### DON'T: Over-lift state
```swift
// Bad - state doesn't need to be in parent
struct ParentView: View {
    @State private var childCounter = 0  // Child could own this

    var body: some View {
        ChildView(counter: $childCounter)
    }
}
```

### DON'T: Create unnecessary ViewModels
```swift
// Bad - simple view doesn't need ViewModel
struct SimpleToggleView: View {
    @ObservedObject var viewModel: SimpleToggleViewModel

    var body: some View {
        Toggle("Enable", isOn: $viewModel.isEnabled)
    }
}

// Good - use @State for simple local state
struct SimpleToggleView: View {
    @State private var isEnabled = false

    var body: some View {
        Toggle("Enable", isOn: $isEnabled)
    }
}
```
