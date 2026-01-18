# View Composition

Build the UI by breaking complex interfaces into small, focused views.

## Core Principles

1. **Extract reusable components naturally**
2. **Use view modifiers for common styling**
3. **Prefer composition over inheritance**
4. **Avoid using `AnyView`** - it hides type information and hurts performance

## Breaking Down Complex Views

### Before (Monolithic)
```swift
struct ProfileView: View {
    var body: some View {
        VStack {
            // 100+ lines of header code
            // 50+ lines of stats code
            // 80+ lines of actions code
        }
    }
}
```

### After (Composed)
```swift
struct ProfileView: View {
    @ObservedObject var viewModel: ProfileViewModel

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                ProfileHeaderView(user: viewModel.user)
                ProfileStatsView(stats: viewModel.stats)
                ProfileActionsView(onAction: viewModel.handleAction)
            }
        }
    }
}
```

## Extracting Subviews

### Private Computed Properties
For view-specific decomposition:

```swift
struct ProfileView: View {
    var body: some View {
        VStack {
            headerSection
            contentSection
            footerSection
        }
    }

    private var headerSection: some View {
        HStack {
            // Header content
        }
    }

    private var contentSection: some View {
        VStack {
            // Content
        }
    }
}
```

### Separate Structs
For reusable components:

```swift
struct ProfileHeaderView: View {
    let user: User

    var body: some View {
        HStack {
            AsyncImage(url: user.avatarURL)
            VStack(alignment: .leading) {
                Text(user.name).font(.headline)
                Text(user.email).font(.subheadline)
            }
        }
    }
}
```

## View Modifiers

### Custom Modifiers
```swift
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(Color.white)
            .cornerRadius(12)
            .shadow(radius: 4)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
}

// Usage
Text("Hello").cardStyle()
```

## Avoiding AnyView

### DON'T
```swift
func getContent() -> AnyView {
    if showDetail {
        return AnyView(DetailView())
    } else {
        return AnyView(SummaryView())
    }
}
```

### DO - Use @ViewBuilder
```swift
@ViewBuilder
var content: some View {
    if showDetail {
        DetailView()
    } else {
        SummaryView()
    }
}
```

### DO - Use Generic Types
```swift
struct Container<Content: View>: View {
    let content: Content

    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }

    var body: some View {
        VStack {
            content
        }
    }
}
```

## Composition Patterns

### Slot Pattern
```swift
struct Card<Header: View, Content: View>: View {
    let header: Header
    let content: Content

    init(
        @ViewBuilder header: () -> Header,
        @ViewBuilder content: () -> Content
    ) {
        self.header = header()
        self.content = content()
    }

    var body: some View {
        VStack {
            header
            Divider()
            content
        }
    }
}

// Usage
Card {
    Text("Title")
} content: {
    Text("Body content here")
}
```

### Modifier Chain
```swift
Text("Hello")
    .font(.headline)
    .foregroundColor(.blue500)
    .padding()
    .background(Color.gray100)
    .cornerRadius(8)
```

## Best Practices

- Keep views focused on one responsibility
- Pass data down, actions up
- Use environment for truly global state
- Prefer value types (structs) for view data
- Use `@ViewBuilder` for conditional content
