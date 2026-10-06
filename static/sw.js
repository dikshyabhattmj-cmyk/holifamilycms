/* ==========================================================================
   Holi Family Secondary School - Service Worker
   Comprehensive PWA Offline Caching + Background Web Push Notifications
   ========================================================================== */

const CACHE_NAME = 'hfss-pwa-v1.4.0';
const OFFLINE_URL = '/';

const PRECACHE_ASSETS = [
  '/static/css/main.css',
  '/static/js/main.js',
  '/static/js/pwa.js',
  '/static/audio/notification.wav',
  '/static/manifest.json',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/static/icons/badge-96x96.png'
];

// Install Event: Precaches core shell assets
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn('[SW] Pre-caching partial warning:', err);
      });
    })
  );
});

// Activate Event: Cleans old caches and claims active clients
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            console.log('[SW] Purging outdated cache:', name);
            return caches.delete(name);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Stale-While-Revalidate for CSS/JS/images, Network-First for HTML navigation
self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // Skip non-HTTP / browser extension schemes
  if (!url.protocol.startsWith('http')) return;

  // HTML page navigation: Network-first with cache fallback
  if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
          }
          return response;
        })
        .catch(() => {
          return caches.match(request).then((cachedResponse) => {
            return cachedResponse || caches.match(OFFLINE_URL);
          });
        })
    );
    return;
  }

  // Static Assets (CSS, JS, Fonts, Images, Audio): Cache-first with background refresh
  if (
    url.pathname.startsWith('/static/') ||
    url.hostname.includes('fonts.googleapis.com') ||
    url.hostname.includes('fonts.gstatic.com') ||
    url.hostname.includes('cdnjs.cloudflare.com') ||
    url.hostname.includes('cdn.jsdelivr.net')
  ) {
    event.respondWith(
      caches.match(request).then((cachedResponse) => {
        const fetchPromise = fetch(request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          }
          return networkResponse;
        }).catch(() => null);

        return cachedResponse || fetchPromise;
      })
    );
  }
});

// =========================================================================
// Real-Time Web Push Notification Handler
// Works when app/browser is completely closed, locked screen, mobile & desktop
// =========================================================================

self.addEventListener('push', (event) => {
  let data = {
    title: 'Holi Family Secondary School',
    body: 'New announcement or update from school administration.',
    url: '/',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/badge-96x96.png',
    sound: '/static/audio/notification.wav',
    tag: 'hf-update',
    renotify: true
  };

  if (event.data) {
    try {
      const parsed = event.data.json();
      data = { ...data, ...parsed };
    } catch (e) {
      data.body = event.data.text() || data.body;
    }
  }

  const notificationOptions = {
    body: data.body,
    icon: data.icon || '/static/icons/icon-192x192.png',
    badge: data.badge || '/static/icons/badge-96x96.png',
    sound: data.sound || '/static/audio/notification.wav',
    tag: data.tag || 'hf-general',
    data: {
      url: data.url || '/'
    },
    // Strong multi-pulse vibration pattern for mobile devices (screen on or off):
    vibrate: [500, 250, 500, 250, 500, 250, 800],
    renotify: true,
    silent: false,
    requireInteraction: true,
    timestamp: Date.now(),
    actions: [
      {
        action: 'open_url',
        title: '🔔 View Notice'
      },
      {
        action: 'dismiss',
        title: 'Dismiss'
      }
    ]
  };

  const notifyPromise = self.registration.showNotification(data.title, notificationOptions);

  // Broadcast to all open tabs/clients to trigger immediate audio chime
  const clientBroadcastPromise = self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clients) => {
    for (const client of clients) {
      client.postMessage({
        type: 'PUSH_RECEIVED',
        data: data
      });
    }
  });

  event.waitUntil(Promise.all([notifyPromise, clientBroadcastPromise]));
});

// Notification Click Event: Opens destination URL in PWA or existing window
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'dismiss') {
    return;
  }

  const targetUrl = (event.notification.data && event.notification.data.url)
    ? event.notification.data.url
    : '/';

  const fullUrl = new URL(targetUrl, self.location.origin).href;

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      // If a window is already open, focus and navigate it
      for (let client of windowClients) {
        if (client.url === fullUrl && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(fullUrl);
      }
    })
  );
});

// Push Subscription Change Event (handles auto-rotation by push services)
self.addEventListener('pushsubscriptionchange', (event) => {
  event.waitUntil(
    self.registration.pushManager.subscribe(event.oldSubscription.options)
      .then((newSubscription) => {
        return fetch('/portal/push/subscribe/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            endpoint: newSubscription.endpoint,
            keys: {
              p256dh: btoa(String.fromCharCode.apply(null, new Uint8Array(newSubscription.getKey('p256dh')))),
              auth: btoa(String.fromCharCode.apply(null, new Uint8Array(newSubscription.getKey('auth'))))
            },
            userAgent: navigator.userAgent
          })
        });
      })
  );
});
