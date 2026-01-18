# Available 3rd Party Integrations

Detailed descriptions of 3rd party services available for integration.

## Backend Services

### Firebase

**Purpose:** Google's mobile development platform

**SPM URL:** `https://github.com/firebase/firebase-ios-sdk.git`

**Products:**
- **FirebaseAuth** - User authentication (email, Apple, Google, phone)
- **FirebaseFirestore** - NoSQL document database
- **FirebaseStorage** - File storage (images, videos, etc.)
- **FirebaseAnalytics** - Event and user analytics
- **FirebaseCrashlytics** - Crash reporting
- **FirebaseMessaging** - Push notifications (FCM)
- **FirebaseRemoteConfig** - Remote configuration

**Setup Required:**
1. Create project at console.firebase.google.com
2. Download GoogleService-Info.plist
3. Add to Xcode project Resources/
4. Call `FirebaseApp.configure()` in App init

---

### Supabase

**Purpose:** Open-source Firebase alternative with PostgreSQL

**SPM URL:** `https://github.com/supabase/supabase-swift.git`

**Features:**
- **Auth** - Email, Apple, Google, magic link, OAuth
- **Database** - PostgreSQL with Row Level Security
- **Storage** - File storage with CDN
- **Realtime** - WebSocket subscriptions
- **Edge Functions** - Serverless functions (Deno)

**Setup Required:**
1. Create project at supabase.com
2. Get project URL and anon key
3. Initialize SupabaseClient in App

**Advantages over Firebase:**
- SQL database (PostgreSQL)
- Self-hostable
- Open source
- Row Level Security built-in

---

## Monetization

### RevenueCat

**Purpose:** Subscription and in-app purchase management

**SPM URL:** `https://github.com/RevenueCat/purchases-ios.git`

**Features:**
- Subscription status checking
- Cross-platform purchase sync
- Subscription analytics
- Paywall A/B testing
- Webhook integrations
- Promo codes

**Setup Required:**
1. Create account at revenuecat.com
2. Set up products in App Store Connect
3. Configure products/offerings in RevenueCat
4. Get API key
5. Call `Purchases.configure()` in App init

**Why Use RevenueCat:**
- Handles receipt validation
- Cross-platform (iOS, Android, web)
- Analytics dashboard
- No server needed

---

## Analytics

### Mixpanel

**Purpose:** Product analytics and user tracking

**SPM URL:** `https://github.com/mixpanel/mixpanel-swift.git`

**Features:**
- Event tracking with properties
- User identification and profiles
- Funnel analysis
- Retention analysis
- A/B testing
- User segmentation

**Setup Required:**
1. Create project at mixpanel.com
2. Get project token
3. Initialize in App init

---

### PostHog

**Purpose:** Product analytics with feature flags

**SPM URL:** `https://github.com/PostHog/posthog-ios.git`

**Features:**
- Event tracking
- Feature flags
- Session recording (optional)
- A/B testing
- User identification
- Self-hostable option

**Setup Required:**
1. Create project at posthog.com (or self-host)
2. Get API key
3. Initialize in App init

**Advantages:**
- Open source
- Self-hostable
- Feature flags included
- Session recording

---

### Amplitude

**Purpose:** Behavioral analytics platform

**SPM URL:** `https://github.com/amplitude/Amplitude-Swift.git`

**Features:**
- Event tracking
- User properties
- Behavioral cohorts
- Funnel analysis
- Revenue tracking

**Setup Required:**
1. Create project at amplitude.com
2. Get API key
3. Initialize in App init

---

## Push Notifications

### OneSignal

**Purpose:** Push notification service

**SPM URL:** `https://github.com/OneSignal/OneSignal-iOS-SDK.git`

**Features:**
- Push notifications
- In-app messaging
- Email/SMS (additional)
- Segmentation
- A/B testing
- Analytics

**Setup Required:**
1. Create app at onesignal.com
2. Configure iOS app with APNs certificate
3. Get App ID
4. Initialize in App init

---

## Error Tracking

### Sentry

**Purpose:** Error tracking and performance monitoring

**SPM URL:** `https://github.com/getsentry/sentry-cocoa.git`

**Features:**
- Crash reporting
- Error tracking
- Performance monitoring
- Release tracking
- User feedback

**Setup Required:**
1. Create project at sentry.io
2. Get DSN
3. Initialize in App init

---

## Feature Flags

### LaunchDarkly

**Purpose:** Feature flag management

**SPM URL:** `https://github.com/launchdarkly/ios-client-sdk.git`

**Features:**
- Feature flags
- A/B testing
- Targeted rollouts
- Kill switches
- Multivariate flags

**Setup Required:**
1. Create project at launchdarkly.com
2. Get mobile SDK key
3. Initialize in App init

---

## Images

### Kingfisher

**Purpose:** Async image loading and caching for SwiftUI/UIKit

**SPM URL:** `https://github.com/onevcat/Kingfisher.git`

**Features:**
- Async image downloading
- Memory and disk caching
- Image processing (resize, crop, blur, etc.)
- Placeholder and error image support
- Animated image support (GIF)
- SwiftUI native (`KFImage`)
- UIKit support (`UIImageView` extension)
- Prefetching for lists

**Setup Required:**
- None, just import and use

**Why Use Kingfisher:**
- Battle-tested and widely used
- Excellent caching strategy
- Built-in image processing
- Native SwiftUI support

---

## Integration Comparison

| Service | Best For | Pricing |
|---------|----------|---------|
| Firebase | Quick prototyping, Google ecosystem | Free tier + pay as you go |
| Supabase | SQL database, self-hosting option | Free tier + pay as you go |
| RevenueCat | Subscriptions | Free < $2.5k MTR |
| Mixpanel | Detailed analytics | Free tier available |
| PostHog | Open source, feature flags | Free self-hosted |
| Sentry | Error tracking | Free tier available |
| Kingfisher | Image loading/caching | Free (MIT) |

## Common Combinations

### Indie App Stack
- Supabase (backend)
- RevenueCat (subscriptions)
- PostHog (analytics + feature flags)

### Enterprise Stack
- Firebase (backend)
- RevenueCat (subscriptions)
- Mixpanel (analytics)
- LaunchDarkly (feature flags)
- Sentry (error tracking)

### Minimal Stack
- Supabase (backend + auth)
- RevenueCat (if subscriptions needed)
