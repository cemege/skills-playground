---
name: ios-integration-setup
description: Add 3rd party integrations to an iOS project. Firebase, Supabase, RevenueCat, analytics, and other external services.
type: workflow
---

# iOS Integration Setup

Add 3rd party services and integrations to iOS projects.

## Core Philosophy

- **Developer choice** - Ask what integrations are needed, don't assume
- **3rd party only** - Core packages (Network, Extensions) are handled by `ios-project-init`
- **Guided setup** - Provide configuration steps for each service

## When to Use This Skill

Use this skill when:
- Adding Firebase, Supabase, or other backend services
- Setting up RevenueCat for subscriptions
- Integrating analytics (Mixpanel, PostHog, Amplitude)
- Adding any external SDK or service

**Note:** For core packages (Network, Extensions), use `ios-project-init` instead.

## Workflow

### Step 1: Ask Which Integrations Needed

Present available 3rd party integrations:

**Backend Services:**
- [ ] **Firebase** - Auth, Firestore, Storage, Analytics, Crashlytics
- [ ] **Supabase** - Auth, Database, Storage, Edge Functions

**Monetization:**
- [ ] **RevenueCat** - Subscription management and paywalls

**Analytics:**
- [ ] **Mixpanel** - Event tracking and user analytics
- [ ] **PostHog** - Product analytics with feature flags
- [ ] **Amplitude** - Behavioral analytics

**Push Notifications:**
- [ ] **OneSignal** - Push notification service
- [ ] **Firebase Cloud Messaging** - (included with Firebase)

**Images:**
- [ ] **Kingfisher** - Async image loading and caching

**Other:**
- [ ] **Sentry** - Error tracking and monitoring
- [ ] **LaunchDarkly** - Feature flags

### Step 2: Add Dependencies

For each selected integration, add via Swift Package Manager:

```swift
// Package.swift or Xcode SPM
dependencies: [
    // Firebase
    .package(url: "https://github.com/firebase/firebase-ios-sdk.git", from: "11.0.0"),

    // Supabase
    .package(url: "https://github.com/supabase/supabase-swift.git", from: "2.0.0"),

    // RevenueCat
    .package(url: "https://github.com/RevenueCat/purchases-ios.git", from: "5.0.0"),

    // Mixpanel
    .package(url: "https://github.com/mixpanel/mixpanel-swift.git", from: "4.0.0"),

    // PostHog
    .package(url: "https://github.com/PostHog/posthog-ios.git", from: "3.0.0"),

    // Kingfisher
    .package(url: "https://github.com/onevcat/Kingfisher.git", from: "8.0.0"),
]
```

### Step 3: Provide Setup Instructions

For each integration, provide:
1. Required configuration files
2. App initialization code
3. Environment variables needed
4. Basic usage examples

## Integration Setup Guides

### Firebase

**Requirements:**
- GoogleService-Info.plist in Resources/
- Firebase project at console.firebase.google.com

**App Setup:**
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

**Products:**
- FirebaseAuth
- FirebaseFirestore
- FirebaseStorage
- FirebaseAnalytics
- FirebaseCrashlytics

---

### Supabase

**Requirements:**
- Supabase project URL
- Supabase anon key

**App Setup:**
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
```

**Features:**
- Auth (email, Apple, Google, magic link)
- Database (PostgreSQL)
- Storage (with CDN)
- Realtime subscriptions
- Edge Functions

---

### RevenueCat

**Requirements:**
- RevenueCat API key
- Products configured in App Store Connect
- Offerings configured in RevenueCat dashboard

**App Setup:**
```swift
import SwiftUI
import RevenueCat

@main
struct MyApp: App {
    init() {
        Purchases.configure(withAPIKey: "your-api-key")
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

**Features:**
- Subscription status
- Purchase flow
- Restore purchases
- Entitlement checking

---

### Mixpanel

**Requirements:**
- Mixpanel project token

**App Setup:**
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

**Usage:**
```swift
Mixpanel.mainInstance().track(event: "Button Tapped", properties: ["name": "signup"])
Mixpanel.mainInstance().identify(distinctId: userId)
```

---

### PostHog

**Requirements:**
- PostHog API key
- PostHog host (cloud or self-hosted)

**App Setup:**
```swift
import SwiftUI
import PostHog

@main
struct MyApp: App {
    init() {
        let config = PostHogConfig(apiKey: "your-api-key", host: "https://app.posthog.com")
        PostHogSDK.shared.setup(config)
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

**Usage:**
```swift
PostHogSDK.shared.capture("user_signed_up", properties: ["method": "apple"])
PostHogSDK.shared.isFeatureEnabled("new_onboarding")
```

---

### Sentry

**Requirements:**
- Sentry DSN

**App Setup:**
```swift
import SwiftUI
import Sentry

@main
struct MyApp: App {
    init() {
        SentrySDK.start { options in
            options.dsn = "your-dsn"
            options.tracesSampleRate = 1.0
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Kingfisher

**Requirements:**
- None (just add SPM dependency)

**Usage:**
```swift
import SwiftUI
import Kingfisher

struct AvatarView: View {
    let url: URL?

    var body: some View {
        KFImage(url)
            .placeholder {
                ProgressView()
            }
            .resizable()
            .aspectRatio(contentMode: .fill)
            .frame(width: 48, height: 48)
            .clipShape(Circle())
    }
}
```

**Features:**
- Async image downloading
- Memory and disk caching
- Placeholder and error handling
- Image processing (resize, blur, etc.)
- SwiftUI native support

---

## Example Conversation

**Claude:** What 3rd party integrations do you need?

- [ ] Firebase
- [ ] Supabase
- [ ] RevenueCat
- [ ] Mixpanel
- [ ] PostHog
- [ ] Sentry
- [ ] Other

**Developer:** Firebase and RevenueCat

**Claude:** I'll set up Firebase and RevenueCat:

1. Adding SPM dependencies...
2. Firebase requires GoogleService-Info.plist - have you created a Firebase project?
3. RevenueCat requires API key - have you set up RevenueCat dashboard?

Let me generate the setup code...

## References

- [Available Packages](references/available-packages.md) - 3rd party integration details
- [Package Usage](references/package-usage.md) - Usage examples

## Related Skills

- `ios-project-init` - For core packages (Network, Extensions)
- `swiftui-guidelines` - For implementing features with these integrations
