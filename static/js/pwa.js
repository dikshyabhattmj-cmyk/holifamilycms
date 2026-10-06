/**
 * ==========================================================================
 * Holi Family Secondary School - PWA & Web Push Notification Client Module
 * Supports: Android Chrome/Firefox/Edge, iOS Safari (16.4+), Desktop, Tablets
 * ==========================================================================
 */

class HFPWAManager {
  constructor() {
    this.deferredPrompt = null;
    this.swRegistration = null;
    this.vapidPublicKey = null;
    this.isSubscribed = false;
    this.isStandalone = window.matchMedia('(display-mode: standalone)').matches || 
                        window.navigator.standalone === true || 
                        document.referrer.includes('android-app://');
    this.isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    this.isAndroid = /Android/.test(navigator.userAgent);
    
    this.audioAlert = new Audio('/static/audio/notification.wav');
    this.audioAlert.preload = 'auto';
    this.audioUnlocked = false;
    
    this.init();
    this.setupAudioUnlock();
  }

  async init() {
    this.setupInstallListeners();
    this.registerServiceWorker();
    this.setupNotificationUI();
    this.setupServiceWorkerMessageListener();
  }

  setupAudioUnlock() {
    const unlockAudio = () => {
      if (this.audioUnlocked) return;
      try {
        if (this.audioAlert) {
          this.audioAlert.volume = 1.0;
          this.audioAlert.play().then(() => {
            this.audioAlert.pause();
            this.audioAlert.currentTime = 0;
            this.audioUnlocked = true;
          }).catch(() => {});
        }
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) {
          const ctx = new AudioCtx();
          if (ctx.state === 'suspended') {
            ctx.resume();
          }
          this.audioUnlocked = true;
        }
      } catch (e) {}
      ['click', 'touchstart', 'keydown'].forEach(evt => {
        document.removeEventListener(evt, unlockAudio);
      });
    };

    ['click', 'touchstart', 'keydown'].forEach(evt => {
      document.addEventListener(evt, unlockAudio, { once: true, passive: true });
    });
  }

  playNotificationSound() {
    try {
      this.synthesizeChime();
      if (this.audioAlert) {
        this.audioAlert.currentTime = 0;
        this.audioAlert.volume = 1.0;
        this.audioAlert.play().catch(() => {});
      }
    } catch (e) {
      this.synthesizeChime();
    }
  }

  synthesizeChime() {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      if (ctx.state === 'suspended') ctx.resume();
      const now = ctx.currentTime;
      
      // Powerful clear harmonic chime (C6 - 1046.5Hz, E6 - 1318.5Hz, G6 - 1567.98Hz, C7 - 2093Hz)
      const freqs = [1046.5, 1318.5, 1567.98, 2093.0];
      freqs.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, now + idx * 0.1);
        
        gain.gain.setValueAtTime(0.001, now + idx * 0.1);
        gain.gain.exponentialRampToValueAtTime(0.5, now + idx * 0.1 + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + idx * 0.1 + 0.45);
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        
        osc.start(now + idx * 0.1);
        osc.stop(now + idx * 0.1 + 0.46);
      });
    } catch (err) {
      console.warn('[Audio] Synthesizer error:', err);
    }
  }

  setupServiceWorkerMessageListener() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'PUSH_RECEIVED') {
          console.log('[PWA] Push received on client:', event.data.data);
          this.playNotificationSound();
          if (event.data.data && event.data.data.title) {
            this.showToast(`📢 ${event.data.data.title}: ${event.data.data.body || ''}`, 'info');
          }
        }
      });
    }
  }

  /* ---------------------------------------------------------
   * Service Worker Registration
   * --------------------------------------------------------- */
  async registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.register('/sw.js', {
          scope: '/'
        });
        this.swRegistration = registration;
        console.log('[PWA] Service Worker registered successfully:', registration.scope);

        // Check active push subscription state
        if ('PushManager' in window && 'Notification' in window) {
          this.checkCurrentSubscription();
        }
      } catch (err) {
        console.warn('[PWA] Service Worker registration failed:', err);
      }
    }
  }

  /* ---------------------------------------------------------
   * PWA Installation Flow (Android, Desktop, Chrome, Edge, Safari)
   * --------------------------------------------------------- */
  setupInstallListeners() {
    // Initial display check - hide buttons if already installed
    if (this.isStandalone) {
      this.toggleInstallButtons(false);
      console.log('[PWA] App running in standalone installed mode');
    } else {
      this.toggleInstallButtons(true);
    }

    // Capture standard PWA install event
    window.addEventListener('beforeinstallprompt', (e) => {
      // Prevent the mini-infobar from appearing on mobile
      e.preventDefault();
      // Stash the event so it can be triggered when user clicks the Install App button
      this.deferredPrompt = e;
      console.log('[PWA] Native beforeinstallprompt captured and ready for user trigger');
      if (!this.isStandalone) {
        this.toggleInstallButtons(true);
      }
    });

    window.addEventListener('appinstalled', () => {
      console.log('[PWA] Holy Family App installed successfully');
      this.deferredPrompt = null;
      this.isStandalone = true;
      this.toggleInstallButtons(false);
      this.showToast('🎉 Holy Family App installed successfully on your device!', 'success');
      
      // Close modal if open
      const modalEl = document.getElementById('pwaInstallHelperModal');
      if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
    });

    // Handle clicks on any button with data-pwa-install
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-pwa-install]');
      if (btn) {
        e.preventDefault();
        this.promptInstall();
      }
    });

    // Listen for display-mode changes (e.g. user opens in installed window)
    window.matchMedia('(display-mode: standalone)').addEventListener('change', (evt) => {
      this.isStandalone = evt.matches;
      this.toggleInstallButtons(!this.isStandalone);
    });
  }

  toggleInstallButtons(show) {
    const installBtns = document.querySelectorAll('[data-pwa-install]');
    installBtns.forEach((btn) => {
      if (show && !this.isStandalone) {
        btn.classList.remove('d-none');
        btn.style.display = '';
      } else {
        btn.classList.add('d-none');
        btn.style.display = 'none';
      }
    });
  }

  async promptInstall() {
    if (this.isStandalone) {
      this.showToast('Holy Family App is already installed and running on this device.', 'info');
      this.toggleInstallButtons(false);
      return;
    }

    // 1. If native prompt was captured (Chrome / Edge / Android browsers / supported Desktops)
    if (this.deferredPrompt) {
      try {
        this.deferredPrompt.prompt();
        const choiceResult = await this.deferredPrompt.userChoice;
        if (choiceResult && choiceResult.outcome === 'accepted') {
          console.log('[PWA] User accepted installation prompt');
          this.showToast('Installing Holy Family App...', 'success');
        } else {
          console.log('[PWA] User dismissed installation prompt');
        }
        this.deferredPrompt = null;
        return;
      } catch (err) {
        console.warn('[PWA] Prompt execution error:', err);
      }
    }

    // 2. On platforms without beforeinstallprompt (e.g., iOS Safari or non-Chromium browsers)
    this.showInstallHelperModal();
  }

  showInstallHelperModal() {
    let modalEl = document.getElementById('pwaInstallHelperModal');
    if (!modalEl) {
      const modalHtml = `
        <div class="modal fade" id="pwaInstallHelperModal" tabindex="-1" aria-labelledby="pwaInstallHelperModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content rounded-4 border-0 shadow-lg">
              <div class="modal-header border-0 pb-0">
                <h5 class="modal-title fw-bold text-dark d-flex align-items-center gap-2" id="pwaInstallHelperModalLabel">
                  <i class="fa-solid fa-download text-primary"></i> Install Holy Family App
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body text-center py-4">
                <img src="/static/icons/icon-192x192.png" alt="Holy Family App Icon" class="rounded-4 shadow-sm mb-3" style="width: 72px; height: 72px;">
                <h6 class="fw-bold mb-2">Fast, Lightweight & Works Offline</h6>
                <p class="text-muted small mb-4">Install our official application on your phone, tablet, or desktop for instant access, exam routines, and real-time notices.</p>
                
                <div class="text-start bg-light p-3 rounded-3 border small mb-4">
                  ${this.isIOS ? `
                    <div class="mb-2"><strong>📱 Apple iOS (Safari):</strong></div>
                    <ol class="ps-3 mb-0 text-muted">
                      <li class="mb-1">Tap the <strong>Share</strong> button at the bottom toolbar (<i class="fa-solid fa-arrow-up-from-bracket text-primary"></i>).</li>
                      <li class="mb-1">Scroll down and tap <strong>Add to Home Screen</strong> (<i class="fa-regular fa-square-plus text-primary"></i>).</li>
                      <li>Tap <strong>Add</strong> at the top right corner to install.</li>
                    </ol>
                  ` : `
                    <div class="mb-2"><strong>💻 Android & Desktop (Chrome / Edge):</strong></div>
                    <ul class="ps-3 mb-0 text-muted">
                      <li class="mb-1">Click or tap the browser menu (<strong>⋮</strong> or <strong>…</strong>) in the top right.</li>
                      <li class="mb-1">Select <strong>Install Holy Family...</strong> or <strong>Add to Home Screen</strong>.</li>
                      <li>Confirm when the browser prompt asks to install.</li>
                    </ul>
                  `}
                </div>
                <button type="button" class="btn btn-hf-primary btn-sm px-4 rounded-pill" data-bs-dismiss="modal">Got it, thanks!</button>
              </div>
            </div>
          </div>
        </div>
      `;
      document.body.insertAdjacentHTML('beforeend', modalHtml);
      modalEl = document.getElementById('pwaInstallHelperModal');
    }

    if (modalEl && window.bootstrap) {
      const modal = new bootstrap.Modal(modalEl);
      modal.show();
    }
  }

  /* ---------------------------------------------------------
   * Web Push Notifications System
   * --------------------------------------------------------- */
  async checkCurrentSubscription() {
    if (!this.swRegistration) return;

    try {
      const serverKey = await this.fetchVapidKey();
      const subscription = await this.swRegistration.pushManager.getSubscription();

      let needsResubscribe = false;
      const storedKey = localStorage.getItem('hf_active_vapid_key');

      if (subscription && storedKey && serverKey && storedKey !== serverKey) {
        console.log('[Push] VAPID key rotated on server. Refreshing subscription...');
        needsResubscribe = true;
        await subscription.unsubscribe().catch(() => {});
      }

      if (needsResubscribe || (!subscription && ('Notification' in window) && Notification.permission === 'granted')) {
        await this.subscribeUser();
      } else if (subscription) {
        this.isSubscribed = true;
        this.updateNotificationUI();
        this.sendSubscriptionToServer(subscription);
      }
    } catch (error) {
      console.warn('[Push] Error checking subscription:', error);
    }
  }

  async fetchVapidKey() {
    if (this.vapidPublicKey) return this.vapidPublicKey;
    try {
      const res = await fetch('/portal/push/vapid-public-key/');
      const data = await res.json();
      this.vapidPublicKey = data.publicKey;
      return this.vapidPublicKey;
    } catch (err) {
      console.error('[Push] Failed to fetch VAPID key:', err);
      return null;
    }
  }

  urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  async subscribeUser() {
    if (!('Notification' in window)) {
      this.showToast('Push Notifications are not supported by this browser.', 'warning');
      return false;
    }

    // 1. Request Native Permission
    const permission = await Notification.requestPermission();
    if (permission === 'denied') {
      localStorage.setItem('hf_push_denied', 'true');
      this.showToast('Notification permission was denied. You can enable it anytime in browser settings.', 'warning');
      this.updateNotificationUI();
      return false;
    }

    if (permission !== 'granted') {
      return false;
    }

    // Remove denied flag if granted
    localStorage.removeItem('hf_push_denied');

    // 2. Fetch VAPID key & Subscribe via PushManager
    try {
      const vapidKey = await this.fetchVapidKey();
      if (!vapidKey) {
        throw new Error('VAPID public key unavailable');
      }

      const convertedKey = this.urlBase64ToUint8Array(vapidKey);
      const readySW = await navigator.serviceWorker.ready;
      
      // Always unsubscribe any old/mismatched subscription first to guarantee fresh key generation
      try {
        const existingSub = await readySW.pushManager.getSubscription();
        if (existingSub) {
          await existingSub.unsubscribe();
        }
      } catch (unsubErr) {
        console.warn('[Push] Unsubscribe error before fresh subscribe:', unsubErr);
      }

      const subscription = await readySW.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: convertedKey
      });

      console.log('[Push] User subscribed successfully with active VAPID key:', subscription);
      localStorage.setItem('hf_active_vapid_key', vapidKey);
      this.isSubscribed = true;

      // 3. Sync Subscription with Server
      await this.sendSubscriptionToServer(subscription);
      this.updateNotificationUI();
      this.showToast('🔔 Real-time alerts with sound enabled successfully!', 'success');
      return true;
    } catch (err) {
      console.error('[Push] Failed to subscribe user:', err);
      this.showToast('Could not enable notifications. Please check connection and try again.', 'danger');
      return false;
    }
  }

  async unsubscribeUser() {
    try {
      const readySW = await navigator.serviceWorker.ready;
      const subscription = await readySW.pushManager.getSubscription();
      if (subscription) {
        await fetch('/portal/push/unsubscribe/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ endpoint: subscription.endpoint })
        });
        await subscription.unsubscribe();
      }
      this.isSubscribed = false;
      this.updateNotificationUI();
      this.showToast('Notifications turned off.', 'info');
    } catch (err) {
      console.error('[Push] Error unsubscribing:', err);
    }
  }

  async sendSubscriptionToServer(subscription) {
    try {
      const rawKey = subscription.getKey('p256dh');
      const rawAuth = subscription.getKey('auth');

      const p256dh = rawKey ? btoa(String.fromCharCode.apply(null, new Uint8Array(rawKey))) : '';
      const auth = rawAuth ? btoa(String.fromCharCode.apply(null, new Uint8Array(rawAuth))) : '';

      await fetch('/portal/push/subscribe/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          endpoint: subscription.endpoint,
          keys: {
            p256dh: p256dh,
            auth: auth
          },
          userAgent: navigator.userAgent
        })
      });
    } catch (e) {
      console.warn('[Push] Error syncing subscription to server:', e);
    }
  }

  /* ---------------------------------------------------------
   * UI Controls & Notification Banners
   * --------------------------------------------------------- */
  setupNotificationUI() {
    // Check if permission prompt banner should be offered
    const isDenied = localStorage.getItem('hf_push_denied') === 'true';
    const bannerDismissed = sessionStorage.getItem('hf_push_banner_dismissed') === 'true';
    const hasGranted = ('Notification' in window) && Notification.permission === 'granted';

    // Automatically show browser's native Allow / Block notification prompt upon opening device
    if ('Notification' in window && Notification.permission === 'default' && !isDenied) {
      setTimeout(() => {
        this.subscribeUser();
      }, 1000);
    }

    const promptBar = document.getElementById('pushPermissionBanner');
    if (promptBar && !hasGranted && !isDenied && !bannerDismissed && ('Notification' in window)) {
      setTimeout(() => {
        promptBar.classList.remove('d-none');
      }, 1500);
    }

    // Bind enable buttons
    document.querySelectorAll('[data-push-enable]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        this.subscribeUser();
        if (promptBar) promptBar.classList.add('d-none');
      });
    });

    // Bind toggle buttons
    document.querySelectorAll('[data-push-toggle]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        if (this.isSubscribed) {
          this.unsubscribeUser();
        } else {
          this.subscribeUser();
        }
      });
    });

    // Bind banner dismiss
    const dismissBtn = document.getElementById('dismissPushBanner');
    if (dismissBtn && promptBar) {
      dismissBtn.addEventListener('click', () => {
        promptBar.classList.add('d-none');
        sessionStorage.setItem('hf_push_banner_dismissed', 'true');
      });
    }

    this.updateNotificationUI();
  }

  updateNotificationUI() {
    const toggleBtns = document.querySelectorAll('[data-push-toggle]');
    const statusBadges = document.querySelectorAll('[data-push-status]');

    toggleBtns.forEach((btn) => {
      if (this.isSubscribed) {
        btn.innerHTML = '<i class="fa-solid fa-bell-slash text-danger"></i> <span class="text-nowrap">Disable Alerts</span>';
        btn.classList.add('btn-outline-danger');
        btn.classList.remove('btn-outline-primary', 'btn-hf-primary');
      } else {
        btn.innerHTML = '<i class="fa-solid fa-bell text-warning"></i> <span class="text-nowrap">Live Alerts</span>';
        btn.classList.remove('btn-outline-danger');
        btn.classList.add('btn-outline-primary');
      }
    });

    statusBadges.forEach((badge) => {
      if (this.isSubscribed) {
        badge.textContent = 'Active (Receiving Real-Time Push)';
        badge.className = 'badge bg-success-subtle text-success';
      } else {
        badge.textContent = 'Disabled';
        badge.className = 'badge bg-secondary-subtle text-secondary';
      }
    });
  }

  showToast(message, type = 'info') {
    let toastContainer = document.getElementById('hfToastContainer');
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.id = 'hfToastContainer';
      toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
      toastContainer.style.zIndex = '99999';
      document.body.appendChild(toastContainer);
    }

    const toastId = 'toast_' + Date.now();
    const iconClass = type === 'success' ? 'fa-circle-check text-success' : type === 'warning' ? 'fa-triangle-exclamation text-warning' : type === 'danger' ? 'fa-circle-xmark text-danger' : 'fa-circle-info text-primary';
    
    const toastHtml = `
      <div id="${toastId}" class="toast align-items-center bg-white border-0 shadow-lg rounded-4" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex p-2">
          <div class="toast-body d-flex align-items-center gap-2">
            <i class="fa-solid ${iconClass} fs-5"></i>
            <div class="small fw-semibold text-dark">${message}</div>
          </div>
          <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastEl = document.getElementById(toastId);
    if (toastEl && window.bootstrap) {
      const bsToast = new bootstrap.Toast(toastEl, { delay: 6000 });
      bsToast.show();
      toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
    }
  }
}

// Instantiate on load
document.addEventListener('DOMContentLoaded', () => {
  window.hfPWA = new HFPWAManager();
});
