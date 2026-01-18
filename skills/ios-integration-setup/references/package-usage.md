# 3rd Party Integration Usage Guide

Setup and usage examples for each 3rd party integration.

## Firebase

### Full Setup

```swift
// 1. Add to Package.swift or via Xcode SPM
.package(url: "https://github.com/firebase/firebase-ios-sdk.git", from: "11.0.0")

// Products: FirebaseAuth, FirebaseFirestore, FirebaseStorage, FirebaseAnalytics
```

### App Configuration

```swift
import SwiftUI
import FirebaseCore

@main
struct MyApp: App {
    init() {
        FirebaseApp.configure()
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Authentication

```swift
import FirebaseAuth

// Sign up
let result = try await Auth.auth().createUser(withEmail: email, password: password)
let user = result.user

// Sign in
let result = try await Auth.auth().signIn(withEmail: email, password: password)

// Sign in with Apple
let credential = OAuthProvider.credential(
    withProviderID: "apple.com",
    idToken: idTokenString,
    rawNonce: nonce
)
let result = try await Auth.auth().signIn(with: credential)

// Sign out
try Auth.auth().signOut()

// Current user
let currentUser = Auth.auth().currentUser

// Auth state listener
Auth.auth().addStateDidChangeListener { auth, user in
    // Handle state change
}
```

### Firestore

```swift
import FirebaseFirestore

let db = Firestore.firestore()

// Get documents
let snapshot = try await db.collection("items").getDocuments()
let items = snapshot.documents.compactMap { try? $0.data(as: Item.self) }

// Get single document
let doc = try await db.collection("items").document(id).getDocument()
let item = try doc.data(as: Item.self)

// Add document
let ref = try await db.collection("items").addDocument(from: item)

// Update document
try await db.collection("items").document(id).updateData(["title": "New Title"])

// Delete document
try await db.collection("items").document(id).delete()

// Query
let snapshot = try await db.collection("items")
    .whereField("userId", isEqualTo: userId)
    .order(by: "createdAt", descending: true)
    .limit(to: 20)
    .getDocuments()
```

### Storage

```swift
import FirebaseStorage

let storage = Storage.storage()

// Upload
let ref = storage.reference().child("images/\(userId)/avatar.jpg")
let metadata = StorageMetadata()
metadata.contentType = "image/jpeg"
_ = try await ref.putDataAsync(imageData, metadata: metadata)
let downloadURL = try await ref.downloadURL()

// Download URL
let url = try await storage.reference().child("path/to/file").downloadURL()

// Delete
try await storage.reference().child("path/to/file").delete()
```

---

## Supabase

### Full Setup

```swift
// Add to Package.swift or via Xcode SPM
.package(url: "https://github.com/supabase/supabase-swift.git", from: "2.0.0")
```

### App Configuration

```swift
import SwiftUI
import Supabase

let supabase = SupabaseClient(
    supabaseURL: URL(string: "https://your-project.supabase.co")!,
    supabaseKey: "your-anon-key"
)

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.supabaseClient, supabase)
        }
    }
}

// Environment key
struct SupabaseClientKey: EnvironmentKey {
    static let defaultValue: SupabaseClient? = nil
}

extension EnvironmentValues {
    var supabaseClient: SupabaseClient? {
        get { self[SupabaseClientKey.self] }
        set { self[SupabaseClientKey.self] = newValue }
    }
}
```

### Authentication

```swift
// Sign up
let session = try await supabase.auth.signUp(
    email: email,
    password: password
)

// Sign in
let session = try await supabase.auth.signIn(
    email: email,
    password: password
)

// Sign in with Apple
let session = try await supabase.auth.signInWithApple()

// Magic link
try await supabase.auth.signInWithOTP(email: email)

// Sign out
try await supabase.auth.signOut()

// Current session
let session = supabase.auth.currentSession
let user = session?.user
```

### Database

```swift
// Select
let items: [Item] = try await supabase
    .from("items")
    .select()
    .eq("user_id", value: userId)
    .order("created_at", ascending: false)
    .execute()
    .value

// Insert
let newItem: Item = try await supabase
    .from("items")
    .insert(item)
    .select()
    .single()
    .execute()
    .value

// Update
try await supabase
    .from("items")
    .update(["title": "New Title"])
    .eq("id", value: itemId)
    .execute()

// Delete
try await supabase
    .from("items")
    .delete()
    .eq("id", value: itemId)
    .execute()

// Upsert
try await supabase
    .from("items")
    .upsert(item)
    .execute()
```

### Storage

```swift
// Upload
try await supabase.storage
    .from("avatars")
    .upload(
        path: "user-\(userId).jpg",
        file: imageData,
        options: FileOptions(contentType: "image/jpeg")
    )

// Get public URL
let url = supabase.storage
    .from("avatars")
    .getPublicURL(path: "user-\(userId).jpg")

// Download
let data = try await supabase.storage
    .from("avatars")
    .download(path: "user-\(userId).jpg")

// Delete
try await supabase.storage
    .from("avatars")
    .remove(paths: ["user-\(userId).jpg"])
```

---

## RevenueCat

### Full Setup

```swift
// Add to Package.swift or via Xcode SPM
.package(url: "https://github.com/RevenueCat/purchases-ios.git", from: "5.0.0")
```

### App Configuration

```swift
import SwiftUI
import RevenueCat

@main
struct MyApp: App {
    init() {
        Purchases.logLevel = .debug // Remove in production
        Purchases.configure(withAPIKey: "your-api-key")
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Check Subscription

```swift
// Get customer info
let customerInfo = try await Purchases.shared.customerInfo()

// Check entitlement
let isPro = customerInfo.entitlements["pro"]?.isActive ?? false

// Check specific product
let hasMonthly = customerInfo.activeSubscriptions.contains("com.app.monthly")
```

### Get Offerings

```swift
let offerings = try await Purchases.shared.offerings()

if let current = offerings.current {
    // Available packages
    let monthly = current.monthly
    let annual = current.annual
    let lifetime = current.lifetime

    // All packages
    for package in current.availablePackages {
        print(package.storeProduct.localizedTitle)
        print(package.storeProduct.localizedPriceString)
    }
}
```

### Purchase

```swift
// Purchase package
let (_, customerInfo, _) = try await Purchases.shared.purchase(package: package)

if customerInfo.entitlements["pro"]?.isActive == true {
    // Unlock pro features
}

// Purchase product directly
let (_, customerInfo, _) = try await Purchases.shared.purchase(product: storeProduct)
```

### Restore Purchases

```swift
let customerInfo = try await Purchases.shared.restorePurchases()

if customerInfo.entitlements["pro"]?.isActive == true {
    // Restore successful
}
```

### Identify User

```swift
// After user logs in
let (customerInfo, _) = try await Purchases.shared.logIn(userId)

// After user logs out
let customerInfo = try await Purchases.shared.logOut()
```

---

## Mixpanel

### Full Setup

```swift
// Add to Package.swift or via Xcode SPM
.package(url: "https://github.com/mixpanel/mixpanel-swift.git", from: "4.0.0")
```

### App Configuration

```swift
import SwiftUI
import Mixpanel

@main
struct MyApp: App {
    init() {
        Mixpanel.initialize(token: "your-token", trackAutomaticEvents: true)
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Track Events

```swift
// Simple event
Mixpanel.mainInstance().track(event: "Button Tapped")

// Event with properties
Mixpanel.mainInstance().track(
    event: "Purchase Completed",
    properties: [
        "product_id": productId,
        "price": price,
        "currency": "USD"
    ]
)

// Time event
Mixpanel.mainInstance().time(event: "Onboarding")
// ... user completes onboarding
Mixpanel.mainInstance().track(event: "Onboarding") // Duration tracked
```

### User Identity

```swift
// Identify user
Mixpanel.mainInstance().identify(distinctId: userId)

// Set user properties
Mixpanel.mainInstance().people.set(properties: [
    "$name": user.name,
    "$email": user.email,
    "plan": "pro"
])

// Increment property
Mixpanel.mainInstance().people.increment(property: "login_count", by: 1)
```

### Super Properties

```swift
// Set super properties (sent with every event)
Mixpanel.mainInstance().registerSuperProperties([
    "app_version": appVersion,
    "platform": "iOS"
])
```

---

## PostHog

### Full Setup

```swift
// Add to Package.swift or via Xcode SPM
.package(url: "https://github.com/PostHog/posthog-ios.git", from: "3.0.0")
```

### App Configuration

```swift
import SwiftUI
import PostHog

@main
struct MyApp: App {
    init() {
        let config = PostHogConfig(apiKey: "your-api-key")
        config.host = "https://app.posthog.com" // Or self-hosted URL
        PostHogSDK.shared.setup(config)
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Track Events

```swift
// Simple event
PostHogSDK.shared.capture("button_tapped")

// Event with properties
PostHogSDK.shared.capture(
    "purchase_completed",
    properties: [
        "product_id": productId,
        "price": price
    ]
)

// Screen view
PostHogSDK.shared.screen("Home")
```

### Feature Flags

```swift
// Check feature flag
let isEnabled = PostHogSDK.shared.isFeatureEnabled("new_checkout")

// Get feature flag value
let variant = PostHogSDK.shared.getFeatureFlag("checkout_variant") as? String

// Reload feature flags
PostHogSDK.shared.reloadFeatureFlags()
```

### User Identity

```swift
// Identify user
PostHogSDK.shared.identify(
    userId,
    userProperties: [
        "email": email,
        "plan": "pro"
    ]
)

// Reset (on logout)
PostHogSDK.shared.reset()
```

---

## Sentry

### Full Setup

```swift
// Add to Package.swift or via Xcode SPM
.package(url: "https://github.com/getsentry/sentry-cocoa.git", from: "8.0.0")
```

### App Configuration

```swift
import SwiftUI
import Sentry

@main
struct MyApp: App {
    init() {
        SentrySDK.start { options in
            options.dsn = "your-dsn"
            options.debug = true // Remove in production
            options.tracesSampleRate = 1.0
            options.enableAutoSessionTracking = true
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Capture Errors

```swift
// Capture exception
do {
    try riskyOperation()
} catch {
    SentrySDK.capture(error: error)
}

// Capture message
SentrySDK.capture(message: "Something happened")

// Add breadcrumb
let crumb = Breadcrumb()
crumb.category = "ui"
crumb.message = "User tapped button"
crumb.level = .info
SentrySDK.addBreadcrumb(crumb)
```

### User Context

```swift
// Set user
let user = User()
user.userId = userId
user.email = email
SentrySDK.setUser(user)

// Clear user (on logout)
SentrySDK.setUser(nil)
```

### Performance

```swift
// Start transaction
let transaction = SentrySDK.startTransaction(name: "Load Data", operation: "task")

// Add span
let span = transaction.startChild(operation: "http", description: "GET /api/items")
// ... perform request
span.finish()

// Finish transaction
transaction.finish()
```

---

## Kingfisher

### Full Setup

```swift
// Add to Package.swift or via Xcode SPM
.package(url: "https://github.com/onevcat/Kingfisher.git", from: "8.0.0")
```

### Basic Usage (SwiftUI)

```swift
import SwiftUI
import Kingfisher

struct RemoteImage: View {
    let url: URL?

    var body: some View {
        KFImage(url)
            .resizable()
            .aspectRatio(contentMode: .fill)
    }
}
```

### With Placeholder and Error

```swift
KFImage(url)
    .placeholder {
        ProgressView()
    }
    .onFailure { error in
        print("Failed to load: \(error)")
    }
    .resizable()
    .aspectRatio(contentMode: .fill)
```

### Image Processing

```swift
KFImage(url)
    .setProcessor(
        DownsamplingImageProcessor(size: CGSize(width: 200, height: 200))
        |> RoundCornerImageProcessor(cornerRadius: 20)
    )
    .resizable()
    .frame(width: 200, height: 200)
```

### Fade Animation

```swift
KFImage(url)
    .fade(duration: 0.25)
    .resizable()
```

### Prefetching for Lists

```swift
import Kingfisher

struct ItemListView: View {
    let items: [Item]
    let prefetcher = ImagePrefetcher()

    var body: some View {
        List(items) { item in
            ItemRow(item: item)
        }
        .onAppear {
            let urls = items.compactMap { $0.imageURL }
            prefetcher.start(with: urls)
        }
        .onDisappear {
            prefetcher.stop()
        }
    }
}
```

### Cache Management

```swift
// Clear memory cache
KingfisherManager.shared.cache.clearMemoryCache()

// Clear disk cache
KingfisherManager.shared.cache.clearDiskCache()

// Clear all
KingfisherManager.shared.cache.clearCache()

// Check cache size
KingfisherManager.shared.cache.calculateDiskStorageSize { result in
    switch result {
    case .success(let size):
        print("Disk cache size: \(size / 1024 / 1024) MB")
    case .failure(let error):
        print("Error: \(error)")
    }
}
```

### Custom Cache Configuration

```swift
// Configure cache limits
let cache = ImageCache.default
cache.memoryStorage.config.totalCostLimit = 300 * 1024 * 1024 // 300 MB
cache.diskStorage.config.sizeLimit = 1000 * 1024 * 1024 // 1 GB
cache.diskStorage.config.expiration = .days(7)
```

---

## Common Patterns

### Combining Analytics

```swift
// Analytics service that wraps multiple providers
@Observable
final class AnalyticsService {
    func track(_ event: String, properties: [String: Any] = [:]) {
        // Mixpanel
        Mixpanel.mainInstance().track(event: event, properties: properties)

        // PostHog
        PostHogSDK.shared.capture(event, properties: properties)

        // Firebase
        Analytics.logEvent(event, parameters: properties)
    }

    func identify(userId: String, properties: [String: Any] = [:]) {
        Mixpanel.mainInstance().identify(distinctId: userId)
        PostHogSDK.shared.identify(userId, userProperties: properties)
    }
}
```

### Error Handling with Sentry

```swift
func performAction() async {
    do {
        try await riskyAsyncOperation()
    } catch {
        SentrySDK.capture(error: error)
        // Show user-friendly error
    }
}
```
