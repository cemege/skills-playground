# Code Organization

Organize code by feature, not by type.

## File Organization

### DO: Feature-Based
```
Checkout/
├── CheckoutRouter.swift
├── CheckoutViewModel.swift
├── CheckoutVC.swift
├── CheckoutView.swift
└── Contracts/
    └── CheckoutContract.swift
```

### DON'T: Type-Based
```
Views/
├── CheckoutView.swift
├── ProfileView.swift
ViewModels/
├── CheckoutViewModel.swift
├── ProfileViewModel.swift
```

## MARK Comments

Use `// MARK: -` to separate logical sections:

```swift
struct ProfileView: View {
    @ObservedObject var viewModel: ProfileViewModel

    // MARK: - Body

    var body: some View {
        ScrollView {
            content
        }
    }

    // MARK: - Subviews

    private var headerSection: some View {
        // ...
    }

    private var statsSection: some View {
        // ...
    }
}
```

### ViewModel Organization

```swift
final class ProfileViewModel: BaseHostingViewModel<ProfileRouter> {
    // MARK: - Published Properties

    @Published var profile: Profile?

    // MARK: - Private Properties

    private let profileService: ProfileServiceProtocol

    // MARK: - Initialization

    init(service: ProfileServiceProtocol = ProfileService(), router: ProfileRouter) {
        self.profileService = service
        super.init(router: router)
    }

    // MARK: - Public Methods

    func loadProfile() async {
        viewControllerProvider?.showLoading(style: .red)
        defer { viewControllerProvider?.hideLoading() }
        // Fetch and assign profile
    }

    // MARK: - Private Methods

    private func processData(_ data: ProfileData) {
        // ...
    }
}
```

## Extension Organization

Use extensions to organize large files:

```swift
// ProfileView.swift

struct ProfileView: View {
    @ObservedObject var viewModel: ProfileViewModel

    var body: some View {
        content
    }
}

// MARK: - Subviews

private extension ProfileView {
    var content: some View {
        // ...
    }

    var headerSection: some View {
        // ...
    }
}

// MARK: - Actions

private extension ProfileView {
    func handleTap() {
        // ...
    }
}
```

## Naming Conventions

### Views
```swift
struct ProfileView: View { }           // Main view
struct ProfileHeaderView: View { }     // Subview
struct ProfileAvatarView: View { }     // Component
```

### ViewModels
```swift
final class ProfileViewModel { }       // ViewModel
```

### Protocols
```swift
protocol ProfileServiceProtocol { }    // Service protocol
protocol ProfileRouterProtocol { }     // Router protocol
protocol ProfileDelegate { }           // Delegate
```

### Files
```
ProfileView.swift                      // View
ProfileViewModel.swift                 // ViewModel
ProfileRouter.swift                    // Router
ProfileContract.swift                  // Contracts/Delegates
```

## Keep Related Code Together

### DO
```swift
struct ProfileView: View {
    @State private var showingSheet = false

    var body: some View {
        Button("Show") {
            showingSheet = true
        }
        .sheet(isPresented: $showingSheet) {
            SheetContent()
        }
    }
}
```

### DON'T
```swift
// Separate file just for sheet state
class ProfileSheetManager: ObservableObject {
    @Published var showingSheet = false
}
```

## File Length Guidelines

- **Views**: Try to keep under 200 lines
- **ViewModels**: Try to keep under 300 lines
- **Large files**: Break into extensions or extract components
