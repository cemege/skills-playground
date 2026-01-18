# Async Patterns

Use `async/await` as the default for asynchronous operations.

## Core Principles

1. **Use async/await** as the default
2. **Use `.task` selectively** for lifecycle-aware or id-scoped work; prefer VC `viewDidLoad` for one-time loads in UI packages
3. **Avoid Combine** unless absolutely necessary
4. **Handle errors gracefully** with try/catch
5. **Use @MainActor** for UI updates

## .task Modifier

Lifecycle-aware async loading:

```swift
struct ProfileView: View {
    @ObservedObject var viewModel: ProfileViewModel
    @State private var didLoad = false

    var body: some View {
        ProfileContent(profile: viewModel.profile)
            .task {
                guard !didLoad else { return }
                didLoad = true
                await viewModel.fetchProfile()
            }
    }
}
```

For one-time loads in BaseHostingViewController-based scenes, prefer triggering work in `viewDidLoad`.

### .task with ID

Reload when value changes:

```swift
struct DetailView: View {
    let itemId: String
    @ObservedObject var viewModel: DetailViewModel

    var body: some View {
        DetailContent(item: viewModel.item)
            .task(id: itemId) {
                await viewModel.fetchItem(id: itemId)
            }
    }
}
```

## ViewModel Async Methods

```swift
@MainActor
final class ProfileViewModel: BaseHostingViewModel<ProfileRouter> {
    @Published var profile: Profile?
    @Published var errorMessage: String?

    private let profileService: ProfileServiceProtocol

    func fetchProfile() async {
        viewControllerProvider?.showLoading(style: .red)
        defer { viewControllerProvider?.hideLoading() }

        do {
            profile = try await profileService.fetchProfile()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
```

## @MainActor

Ensure UI updates happen on main thread:

### Class-Level
```swift
@MainActor
final class ProfileViewModel: BaseHostingViewModel<ProfileRouter> {
    @Published var profile: Profile?
    // All @Published updates are safe
}
```

### Method-Level
```swift
final class ProfileViewModel: BaseHostingViewModel<ProfileRouter> {
    @Published var profile: Profile?

    func fetchProfile() async {
        let data = await service.fetch() // Background

        await MainActor.run {
            self.profile = data // Main thread
        }
    }
}
```

## Error Handling

```swift
func loadData() async {
    do {
        let result = try await service.fetchData()
        self.data = result
    } catch is CancellationError {
        // Task was cancelled, ignore
    } catch {
        self.error = error
        // Show error UI
    }
}
```

## Parallel Async

```swift
func loadAllData() async {
    async let profile = profileService.fetch()
    async let settings = settingsService.fetch()

    do {
        let (profileResult, settingsResult) = try await (profile, settings)
        self.profile = profileResult
        self.settings = settingsResult
    } catch {
        self.error = error
    }
}
```

## Cancellation

Tasks from `.task` modifier are automatically cancelled when view disappears:

```swift
.task {
    // This is cancelled if view disappears
    await viewModel.fetchLargeData()
}
```

Check for cancellation in long operations:

```swift
func processItems(_ items: [Item]) async throws {
    for item in items {
        try Task.checkCancellation()
        await process(item)
    }
}
```

## Anti-Patterns

### DON'T: Use Combine for simple async
```swift
// Bad
profileService.fetchProfile()
    .receive(on: DispatchQueue.main)
    .sink { completion in } receiveValue: { profile in
        self.profile = profile
    }
    .store(in: &cancellables)

// Good
profile = try await profileService.fetchProfile()
```

### DON'T: Forget @MainActor
```swift
// Bad - may crash
func fetchData() async {
    let data = await service.fetch()
    self.items = data  // NOT main thread!
}

// Good
@MainActor
func fetchData() async {
    let data = await service.fetch()
    self.items = data  // Safe
}
```
