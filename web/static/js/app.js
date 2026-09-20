/**
 * Goa Express - Bus Reservation System Frontend Controller
 * 12-Hour AM/PM Scheduling, 3-Day Horizon, Auth, Payments & E-Tickets
 */

// Application State
const state = {
    currentUser: null,
    locations: { sources: [], destinations: [] },
    buses: [],
    selectedBus: null,
    selectedSeats: new Set(),
    activeBookingToCancel: null,
    pendingCheckoutAfterAuth: false
};

// DOM Elements Cache
const elements = {
    // Nav & Auth
    navTabs: document.querySelectorAll('.nav-tab'),
    tabPanes: document.querySelectorAll('.tab-pane'),
    openAuthModalBtn: document.getElementById('openAuthModalBtn'),
    userProfileMenu: document.getElementById('userProfileMenu'),
    userAvatar: document.getElementById('userAvatar'),
    navUserName: document.getElementById('navUserName'),
    logoutBtn: document.getElementById('logoutBtn'),
    authModal: document.getElementById('authModal'),
    closeAuthModalBtn: document.getElementById('closeAuthModalBtn'),
    toggleSignInBtn: document.getElementById('toggleSignInBtn'),
    toggleSignUpBtn: document.getElementById('toggleSignUpBtn'),
    signInForm: document.getElementById('signInForm'),
    signUpForm: document.getElementById('signUpForm'),
    linkToSignUp: document.getElementById('linkToSignUp'),
    linkToSignIn: document.getElementById('linkToSignIn'),

    // Search & Filter
    searchForm: document.getElementById('busSearchForm'),
    fromSelect: document.getElementById('fromSelect'),
    toSelect: document.getElementById('toSelect'),
    dateSelect: document.getElementById('dateSelect'),
    typeFilter: document.getElementById('typeFilter'),
    swapLocationsBtn: document.getElementById('swapLocationsBtn'),
    resetSearchBtn: document.getElementById('resetSearchBtn'),
    pillToday: document.getElementById('pillToday'),
    pillTomorrow: document.getElementById('pillTomorrow'),
    pillDay3: document.getElementById('pillDay3'),
    busList: document.getElementById('busList'),
    resultsTitle: document.getElementById('resultsTitle'),
    resultsCount: document.getElementById('resultsCount'),
    noBusesPlaceholder: document.getElementById('noBusesPlaceholder'),

    // Seat Modal
    seatModal: document.getElementById('seatModal'),
    closeSeatModalBtn: document.getElementById('closeSeatModalBtn'),
    seatModalBusName: document.getElementById('seatModalBusName'),
    seatModalBusRoute: document.getElementById('seatModalBusRoute'),
    seatModalBusId: document.getElementById('seatModalBusId'),
    seatModalBusType: document.getElementById('seatModalBusType'),
    seatModalFare: document.getElementById('seatModalFare'),
    seatModalDeparture: document.getElementById('seatModalDeparture'),
    coachSeatGrid: document.getElementById('coachSeatGrid'),
    selectedSeatsList: document.getElementById('selectedSeatsList'),
    totalFareAmount: document.getElementById('totalFareAmount'),
    proceedToCheckoutBtn: document.getElementById('proceedToCheckoutBtn'),

    // Checkout & Payment Modal
    checkoutModal: document.getElementById('checkoutModal'),
    closeCheckoutModalBtn: document.getElementById('closeCheckoutModalBtn'),
    backToSeatsBtn: document.getElementById('backToSeatsBtn'),
    passengerForm: document.getElementById('passengerForm'),
    passengerName: document.getElementById('passengerName'),
    passengerPhone: document.getElementById('passengerPhone'),
    passengerEmail: document.getElementById('passengerEmail'),
    checkoutBusName: document.getElementById('checkoutBusName'),
    checkoutBusRoute: document.getElementById('checkoutBusRoute'),
    checkoutDeparture: document.getElementById('checkoutDeparture'),
    checkoutSeats: document.getElementById('checkoutSeats'),
    breakdownBaseFare: document.getElementById('breakdownBaseFare'),
    checkoutTotalFare: document.getElementById('checkoutTotalFare'),
    confirmBookingBtn: document.getElementById('confirmBookingBtn'),
    confirmBookingBtnText: document.getElementById('confirmBookingBtnText'),
    confirmBookingSpinner: document.getElementById('confirmBookingSpinner'),

    // Ticket Modal
    ticketModal: document.getElementById('ticketModal'),
    closeTicketModalBtn: document.getElementById('closeTicketModalBtn'),
    doneTicketBtn: document.getElementById('doneTicketBtn'),
    ticketContentArea: document.getElementById('ticketContentArea'),

    // Manage Bookings
    bookingSearchInput: document.getElementById('bookingSearchInput'),
    searchBookingBtn: document.getElementById('searchBookingBtn'),
    loadAllBookingsBtn: document.getElementById('loadAllBookingsBtn'),
    bookingsResultsList: document.getElementById('bookingsResultsList'),
    noBookingsPlaceholder: document.getElementById('noBookingsPlaceholder'),

    // Cancel Modal
    cancelModal: document.getElementById('cancelModal'),
    closeCancelModalBtn: document.getElementById('closeCancelModalBtn'),
    cancelBookingId: document.getElementById('cancelBookingId'),
    cancelSeatsCheckboxList: document.getElementById('cancelSeatsCheckboxList'),
    abortCancelBtn: document.getElementById('abortCancelBtn'),
    executeCancelBtn: document.getElementById('executeCancelBtn'),

    // Occupancy
    occupancyBusSearch: document.getElementById('occupancyBusSearch'),
    refreshOccupancyBtn: document.getElementById('refreshOccupancyBtn'),
    occupancyTableBody: document.getElementById('occupancyTableBody'),

    // Toast
    toastContainer: document.getElementById('toastContainer')
};

// -------------------------------------------------------------
// Toast Notification Utility
// -------------------------------------------------------------
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? '✓' : '⚠️';
    toast.innerHTML = `<span><strong>${icon}</strong> ${message}</span>`;

    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// -------------------------------------------------------------
// API Helper
// -------------------------------------------------------------
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'same-origin',
            ...options
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`API Error on ${endpoint}:`, error);
        showToast('Network connection error. Please try again.', 'error');
        return { success: false, error: error.message };
    }
}

// -------------------------------------------------------------
// App Initialization
// -------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async () => {
    initNavigation();
    init3DayDateSelector();
    await checkAuthSession();
    await loadLocations();
    await fetchBuses();
    loadOccupancyReports();
    setupEventListeners();
});

function initNavigation() {
    elements.navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.getAttribute('data-tab');

            elements.navTabs.forEach(t => t.classList.remove('active'));
            elements.tabPanes.forEach(pane => pane.classList.remove('active'));

            tab.classList.add('active');
            const activePane = document.getElementById(targetId);
            if (activePane) activePane.classList.add('active');

            if (targetId === 'bookings-tab') {
                loadAllBookings();
            } else if (targetId === 'occupancy-tab') {
                loadOccupancyReports();
            }
        });
    });
}

// -------------------------------------------------------------
// 3-Day Horizon Date Selector
// -------------------------------------------------------------
function init3DayDateSelector() {
    const now = new Date();
    const todayStr = formatDateISO(now);

    const tomorrow = new Date();
    tomorrow.setDate(now.getDate() + 1);
    const tomorrowStr = formatDateISO(tomorrow);

    const day3 = new Date();
    day3.setDate(now.getDate() + 2);
    const day3Str = formatDateISO(day3);

    // Constrain date input
    elements.dateSelect.min = todayStr;
    elements.dateSelect.max = day3Str;
    elements.dateSelect.value = todayStr;

    // Quick Date Pills
    elements.pillToday.textContent = `Today (${formatPillDate(now)})`;
    elements.pillTomorrow.textContent = `Tomorrow (${formatPillDate(tomorrow)})`;
    elements.pillDay3.textContent = `Day 3 (${formatPillDate(day3)})`;

    elements.pillToday.addEventListener('click', () => selectQuickDate(todayStr, elements.pillToday));
    elements.pillTomorrow.addEventListener('click', () => selectQuickDate(tomorrowStr, elements.pillTomorrow));
    elements.pillDay3.addEventListener('click', () => selectQuickDate(day3Str, elements.pillDay3));

    elements.dateSelect.addEventListener('change', () => {
        updateActivePill(elements.dateSelect.value, todayStr, tomorrowStr, day3Str);
        fetchBuses();
    });
}

function selectQuickDate(dateStr, pillElement) {
    document.querySelectorAll('.date-pill').forEach(p => p.classList.remove('active'));
    pillElement.classList.add('active');
    elements.dateSelect.value = dateStr;
    fetchBuses();
}

function updateActivePill(currentVal, todayStr, tomorrowStr, day3Str) {
    document.querySelectorAll('.date-pill').forEach(p => p.classList.remove('active'));
    if (currentVal === todayStr) elements.pillToday.classList.add('active');
    else if (currentVal === tomorrowStr) elements.pillTomorrow.classList.add('active');
    else if (currentVal === day3Str) elements.pillDay3.classList.add('active');
}

function formatDateISO(d) {
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function formatPillDate(d) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${d.getDate()} ${months[d.getMonth()]}`;
}

// -------------------------------------------------------------
// Authentication (Sign In, Sign Up, Session)
// -------------------------------------------------------------
async function checkAuthSession() {
    const data = await apiCall('/api/auth/me');
    if (data.success && data.authenticated && data.user) {
        setLoggedInUser(data.user);
    } else {
        // Check localStorage backup
        const stored = localStorage.getItem('goa_express_user');
        if (stored) {
            try {
                const parsed = JSON.parse(stored);
                setLoggedInUser(parsed);
            } catch (e) {
                setLoggedOut();
            }
        } else {
            setLoggedOut();
        }
    }
}

function setLoggedInUser(user) {
    state.currentUser = user;
    localStorage.setItem('goa_express_user', JSON.stringify(user));

    elements.openAuthModalBtn.classList.add('hidden');
    elements.userProfileMenu.classList.remove('hidden');

    elements.navUserName.textContent = user.name;
    const initials = user.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
    elements.userAvatar.textContent = initials || 'GK';

    // Auto-fill checkout fields if opened
    if (elements.passengerName) elements.passengerName.value = user.name || '';
    if (elements.passengerPhone) elements.passengerPhone.value = user.phone || '';
    if (elements.passengerEmail) elements.passengerEmail.value = user.email || '';
}

function setLoggedOut() {
    state.currentUser = null;
    localStorage.removeItem('goa_express_user');
    elements.openAuthModalBtn.classList.remove('hidden');
    elements.userProfileMenu.classList.add('hidden');
}

async function handleSignIn(e) {
    e.preventDefault();
    const email_or_phone = document.getElementById('signInEmail').value.trim();
    const password = document.getElementById('signInPassword').value;

    const data = await apiCall('/api/auth/signin', {
        method: 'POST',
        body: JSON.stringify({ email_or_phone, password })
    });

    if (data.success) {
        setLoggedInUser(data.user);
        elements.authModal.classList.add('hidden');
        elements.signInForm.reset();
        showToast(`Welcome back, ${data.user.name}!`, 'success');

        if (state.pendingCheckoutAfterAuth) {
            state.pendingCheckoutAfterAuth = false;
            openCheckoutModal();
        }
    } else {
        showToast(data.error || 'Invalid credentials', 'error');
    }
}

async function handleSignUp(e) {
    e.preventDefault();
    const name = document.getElementById('signUpName').value.trim();
    const phone = document.getElementById('signUpPhone').value.trim();
    const email = document.getElementById('signUpEmail').value.trim();
    const password = document.getElementById('signUpPassword').value;

    const data = await apiCall('/api/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ name, phone, email, password })
    });

    if (data.success) {
        setLoggedInUser(data.user);
        elements.authModal.classList.add('hidden');
        elements.signUpForm.reset();
        showToast(`Account created! Welcome, ${data.user.name}!`, 'success');

        if (state.pendingCheckoutAfterAuth) {
            state.pendingCheckoutAfterAuth = false;
            openCheckoutModal();
        }
    } else {
        showToast(data.error || 'Registration failed', 'error');
    }
}

async function handleLogout() {
    await apiCall('/api/auth/logout', { method: 'POST' });
    setLoggedOut();
    showToast('Signed out successfully', 'success');
}

// -------------------------------------------------------------
// Locations (Goa Towns/Villages & Outstation)
// -------------------------------------------------------------
async function loadLocations() {
    const data = await apiCall('/api/locations');
    if (data.success) {
        state.locations = data;

        // Populate From
        elements.fromSelect.innerHTML = '<option value="">All Goa Towns & Villages (Origin)</option>';
        data.sources.forEach(town => {
            const opt = document.createElement('option');
            opt.value = town;
            opt.textContent = town;
            elements.fromSelect.appendChild(opt);
        });

        // Populate To
        elements.toSelect.innerHTML = '<option value="">All Destinations</option>';

        const goaGroup = document.createElement('optgroup');
        goaGroup.label = 'Goa Towns & Coastal Villages';
        data.sources.forEach(town => {
            const opt = document.createElement('option');
            opt.value = town;
            opt.textContent = town;
            goaGroup.appendChild(opt);
        });
        elements.toSelect.appendChild(goaGroup);

        const outstationGroup = document.createElement('optgroup');
        outstationGroup.label = 'Outstation Interstate Destinations';
        data.outstation.forEach(city => {
            const opt = document.createElement('option');
            opt.value = city;
            opt.textContent = city;
            outstationGroup.appendChild(opt);
        });
        elements.toSelect.appendChild(outstationGroup);
    }
}

// -------------------------------------------------------------
// Fetch and Render Buses
// -------------------------------------------------------------
async function fetchBuses() {
    const source = elements.fromSelect.value;
    const destination = elements.toSelect.value;
    const date = elements.dateSelect.value;
    const type = elements.typeFilter.value;

    const params = new URLSearchParams();
    if (source) params.append('source', source);
    if (destination) params.append('destination', destination);
    if (date) params.append('date', date);
    if (type) params.append('type', type);

    elements.resultsCount.textContent = 'Searching timetable...';
    elements.busList.innerHTML = '<div style="text-align:center; padding: 2.5rem; color: #64748b;">Loading scheduled buses...</div>';

    const data = await apiCall(`/api/buses?${params.toString()}`);
    if (data.success) {
        state.buses = data.buses;
        renderBusList(data.buses);
    } else {
        showToast(data.error || 'Failed to load buses', 'error');
    }
}

function renderBusList(buses) {
    elements.busList.innerHTML = '';
    elements.resultsCount.textContent = `${buses.length} scheduled bus(es) found`;

    if (!buses || buses.length === 0) {
        elements.noBusesPlaceholder.classList.remove('hidden');
        return;
    }

    elements.noBusesPlaceholder.classList.add('hidden');

    buses.forEach(bus => {
        const card = document.createElement('div');
        card.className = 'bus-card';

        const isLowSeats = bus.available_seats_count <= 5 && bus.available_seats_count > 0;
        const isSoldOut = bus.available_seats_count === 0;

        let seatsClass = '';
        let seatsText = `${bus.available_seats_count} / ${bus.total_seats} seats available`;
        if (isSoldOut) {
            seatsClass = 'sold-out';
            seatsText = 'Sold Out';
        } else if (isLowSeats) {
            seatsClass = 'low';
            seatsText = `Only ${bus.available_seats_count} seats left!`;
        }

        const typeBadgeClass = bus.bus_type.toLowerCase() === 'sleeper' ? 'badge-sleeper' : 'badge-seater';

        card.innerHTML = `
            <div class="bus-info-main">
                <div class="bus-title-row">
                    <span class="bus-name">${bus.name}</span>
                    <span class="bus-id-tag">${bus.bus_id}</span>
                    <span class="badge ${typeBadgeClass}">${bus.bus_type}</span>
                </div>
                <div class="bus-route">
                    <span>${bus.source}</span>
                    <span class="route-arrow">➔</span>
                    <span>${bus.destination}</span>
                </div>
            </div>

            <div class="bus-timing">
                <div class="time-row">
                    <span class="time-label">Departs:</span>
                    <span class="time-val" style="color:var(--primary);">${bus.departure_display}</span>
                </div>
                <div class="time-row">
                    <span class="time-label">Arrives:</span>
                    <span class="time-val">${bus.arrival_display}</span>
                </div>
            </div>

            <div class="bus-seats-fare">
                <div class="fare-val">₹${Math.round(bus.fare)}</div>
                <div class="seats-status-text ${seatsClass}">${seatsText}</div>
            </div>

            <div class="bus-action">
                <button class="btn btn-primary select-seat-btn" data-bus-id="${bus.bus_id}" ${isSoldOut ? 'disabled' : ''}>
                    ${isSoldOut ? 'Sold Out' : 'Select Seats'}
                </button>
            </div>
        `;

        elements.busList.appendChild(card);
    });

    // Attach click listeners
    document.querySelectorAll('.select-seat-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const busId = btn.getAttribute('data-bus-id');
            openSeatModal(busId);
        });
    });
}

// -------------------------------------------------------------
// Interactive Seat Selection Modal
// -------------------------------------------------------------
async function openSeatModal(busId) {
    const data = await apiCall(`/api/buses/${busId}`);
    if (!data.success) {
        showToast(data.error || 'Unable to load seat layout', 'error');
        return;
    }

    const bus = data.bus;
    state.selectedBus = bus;
    state.selectedSeats.clear();

    elements.seatModalBusName.textContent = bus.name;
    elements.seatModalBusRoute.textContent = `${bus.source} ➔ ${bus.destination}`;
    elements.seatModalBusId.textContent = bus.bus_id;
    elements.seatModalBusType.textContent = bus.bus_type;
    elements.seatModalFare.textContent = `₹${Math.round(bus.fare)}`;
    elements.seatModalDeparture.textContent = bus.departure_display;

    renderCoachLayout(bus);
    updateSelectionSummary();

    elements.seatModal.classList.remove('hidden');
}

function renderCoachLayout(bus) {
    elements.coachSeatGrid.innerHTML = '';
    const cols = 4;
    const totalSeats = bus.total_seats;
    const rows = Math.ceil(totalSeats / cols);

    const seatMap = {};
    bus.seats.forEach(s => {
        seatMap[s.seat_number] = s;
    });

    for (let r = 0; r < rows; r++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'seat-row';

        // Col 0
        const seat1No = r * cols + 1;
        rowDiv.appendChild(createSeatElement(seat1No, seatMap[seat1No], totalSeats));

        // Col 1
        const seat2No = r * cols + 2;
        rowDiv.appendChild(createSeatElement(seat2No, seatMap[seat2No], totalSeats));

        // Center Aisle
        const aisle = document.createElement('div');
        aisle.className = 'aisle-gap';
        aisle.textContent = `R${r + 1}`;
        rowDiv.appendChild(aisle);

        // Col 2
        const seat3No = r * cols + 3;
        rowDiv.appendChild(createSeatElement(seat3No, seatMap[seat3No], totalSeats));

        // Col 3
        const seat4No = r * cols + 4;
        rowDiv.appendChild(createSeatElement(seat4No, seatMap[seat4No], totalSeats));

        elements.coachSeatGrid.appendChild(rowDiv);
    }
}

function createSeatElement(seatNo, seatData, totalSeats) {
    if (seatNo > totalSeats || !seatData) {
        return document.createElement('div');
    }

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'seat-btn';
    btn.id = `seat-btn-${seatNo}`;

    const isWindow = seatData.seat_type === 'window';
    const tagText = isWindow ? 'WIN' : 'AIS';

    if (seatData.is_reserved) {
        btn.classList.add('seat-reserved');
        btn.disabled = true;
        btn.title = `Seat ${seatNo} (${seatData.seat_type}) - Reserved`;
    } else {
        btn.classList.add('seat-available');
        btn.title = `Seat ${seatNo} (${seatData.seat_type}) - Click to select`;
        btn.addEventListener('click', () => toggleSeatSelection(seatNo, btn));
    }

    btn.innerHTML = `
        <span class="seat-number">${seatNo}</span>
        <span class="seat-tag">${tagText}</span>
    `;

    return btn;
}

function toggleSeatSelection(seatNo, btnElement) {
    if (state.selectedSeats.has(seatNo)) {
        state.selectedSeats.delete(seatNo);
        btnElement.classList.remove('seat-selected');
        btnElement.classList.add('seat-available');
    } else {
        state.selectedSeats.add(seatNo);
        btnElement.classList.remove('seat-available');
        btnElement.classList.add('seat-selected');
    }
    updateSelectionSummary();
}

function updateSelectionSummary() {
    const selectedArray = Array.from(state.selectedSeats).sort((a, b) => a - b);

    if (selectedArray.length === 0) {
        elements.selectedSeatsList.textContent = 'None';
        elements.totalFareAmount.textContent = '₹0.00';
        elements.proceedToCheckoutBtn.disabled = true;
    } else {
        elements.selectedSeatsList.textContent = selectedArray.join(', ');
        const total = selectedArray.length * (state.selectedBus ? state.selectedBus.fare : 0);
        elements.totalFareAmount.textContent = `₹${total.toFixed(2)}`;
        elements.proceedToCheckoutBtn.disabled = false;
    }
}

// -------------------------------------------------------------
// Checkout, Auth Guard & Payment
// -------------------------------------------------------------
function handleProceedToCheckout() {
    if (!state.selectedBus || state.selectedSeats.size === 0) return;

    // Check if user is signed in
    if (!state.currentUser) {
        state.pendingCheckoutAfterAuth = true;
        elements.seatModal.classList.add('hidden');
        openAuthModal('Please sign in or register to book your bus tickets');
        return;
    }

    openCheckoutModal();
}

function openCheckoutModal() {
    if (!state.selectedBus || state.selectedSeats.size === 0) return;

    elements.seatModal.classList.add('hidden');
    elements.checkoutModal.classList.remove('hidden');

    const bus = state.selectedBus;
    const selectedArray = Array.from(state.selectedSeats).sort((a, b) => a - b);
    const total = selectedArray.length * bus.fare;

    elements.checkoutBusName.textContent = `${bus.name} (${bus.bus_id})`;
    elements.checkoutBusRoute.textContent = `${bus.source} ➔ ${bus.destination}`;
    elements.checkoutDeparture.textContent = bus.departure_display;
    elements.checkoutSeats.textContent = selectedArray.join(', ');

    elements.breakdownBaseFare.textContent = `₹${total.toFixed(2)}`;
    elements.checkoutTotalFare.textContent = `₹${total.toFixed(2)}`;

    // Populate user profile info
    if (state.currentUser) {
        elements.passengerName.value = state.currentUser.name || '';
        elements.passengerPhone.value = state.currentUser.phone || '';
        elements.passengerEmail.value = state.currentUser.email || '';
    }
}

async function handleBookingSubmit(e) {
    e.preventDefault();
    if (!state.selectedBus || state.selectedSeats.size === 0) return;

    const name = elements.passengerName.value.trim();
    const phone = elements.passengerPhone.value.trim();
    const email = elements.passengerEmail.value.trim();
    const selectedPaymentInput = document.querySelector('input[name="paymentMethod"]:checked');
    const paymentMode = selectedPaymentInput ? selectedPaymentInput.value : 'UPI (GPay / PhonePe)';

    if (!name || !phone || !email) {
        showToast('Please fill all passenger details', 'error');
        return;
    }

    // Set loading state
    elements.confirmBookingBtn.disabled = true;
    elements.confirmBookingBtnText.textContent = 'Processing Payment & Booking...';

    const transactionId = `TXN-${Date.now().toString().slice(-8)}`;

    const payload = {
        bus_id: state.selectedBus.bus_id,
        name: name,
        phone: phone,
        email: email,
        seats: Array.from(state.selectedSeats),
        payment_mode: paymentMode,
        transaction_id: transactionId
    };

    const data = await apiCall('/api/bookings', {
        method: 'POST',
        body: JSON.stringify(payload)
    });

    elements.confirmBookingBtn.disabled = false;
    elements.confirmBookingBtnText.textContent = 'Pay & Confirm Booking';

    if (data.success) {
        elements.checkoutModal.classList.add('hidden');
        elements.passengerForm.reset();
        state.selectedSeats.clear();

        showToast('Payment Successful! E-Ticket Generated.', 'success');
        renderTicketReceipt(data.reservation, data.bus_details);
        elements.ticketModal.classList.remove('hidden');

        // Refresh bus data
        fetchBuses();
        loadOccupancyReports();
    } else {
        showToast(data.error || 'Failed to complete booking', 'error');
    }
}

// -------------------------------------------------------------
// Digital E-Ticket Boarding Pass
// -------------------------------------------------------------
function renderTicketReceipt(reservation, busDetails) {
    const seatsStr = reservation.seat_numbers.join(', ');
    const departure = busDetails ? busDetails.departure_display : '--';
    const arrival = busDetails ? busDetails.arrival_display : '--';
    const busName = busDetails ? busDetails.name : reservation.bus_id;
    const busRoute = busDetails ? busDetails.route : 'Goa Route';
    const busType = busDetails ? busDetails.bus_type : 'Express';

    elements.ticketContentArea.innerHTML = `
        <div class="ticket-card">
            <div class="ticket-header">
                <div>
                    <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; opacity:0.85;">GOA EXPRESS • OFFICIAL E-TICKET</div>
                    <div class="ticket-booking-id">${reservation.booking_id}</div>
                </div>
                <div style="text-align:right;">
                    <span class="badge badge-success">Confirmed & Paid</span>
                </div>
            </div>

            <div class="ticket-body">
                <div class="ticket-field">
                    <span class="ticket-field-label">Passenger Name</span>
                    <span class="ticket-field-val">${reservation.user.name}</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Contact</span>
                    <span class="ticket-field-val">${reservation.user.phone}</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Bus Service & Type</span>
                    <span class="ticket-field-val">${busName} (${busType})</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Route</span>
                    <span class="ticket-field-val">${busRoute}</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Departure (12h AM/PM)</span>
                    <span class="ticket-field-val" style="color:var(--primary); font-size:1.05rem;">${departure}</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Estimated Arrival</span>
                    <span class="ticket-field-val">${arrival}</span>
                </div>

                <div class="ticket-divider"></div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Booked Seats</span>
                    <span class="ticket-field-val"><strong class="ticket-seats-highlight">${seatsStr}</strong></span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Total Fare Paid</span>
                    <span class="ticket-field-val" style="color:var(--primary); font-size:1.25rem;">₹${reservation.total_fare.toFixed(2)}</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Payment Method</span>
                    <span class="ticket-field-val">${reservation.payment_mode || 'UPI Instant'}</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Transaction ID</span>
                    <span class="ticket-field-val" style="font-family:monospace; font-size:0.9rem;">${reservation.transaction_id || 'TXN-CONFIRMED'}</span>
                </div>

                <div class="ticket-field" style="grid-column:span 2; margin-top:0.25rem; font-size:0.8rem; color:#64748b; text-align:center;">
                    <span>Please show this digital E-Ticket or SMS on boarding. Booked on ${reservation.booking_time_display || reservation.booking_time}.</span>
                </div>
            </div>
        </div>
    `;
}

// -------------------------------------------------------------
// My Bookings & Manage
// -------------------------------------------------------------
async function loadAllBookings() {
    elements.bookingsResultsList.innerHTML = '<div style="text-align:center; padding: 2.5rem; color: #64748b;">Loading reservations...</div>';
    const data = await apiCall('/api/reservations');
    if (data.success) {
        renderBookingsList(data.reservations);
    }
}

async function searchBookings() {
    const query = elements.bookingSearchInput.value.trim();
    if (!query) {
        loadAllBookings();
        return;
    }

    elements.bookingsResultsList.innerHTML = '<div style="text-align:center; padding: 2.5rem; color: #64748b;">Searching...</div>';

    if (query.toUpperCase().startsWith('BKG') || query.toUpperCase().startsWith('PRE')) {
        const data = await apiCall(`/api/reservations/${query}`);
        if (data.success) {
            renderBookingsList([data.reservation]);
            return;
        }
    }

    const params = new URLSearchParams();
    if (/^\d+$/.test(query)) {
        params.append('phone', query);
    } else {
        params.append('name', query);
    }

    const data = await apiCall(`/api/reservations/search?${params.toString()}`);
    if (data.success) {
        renderBookingsList(data.reservations);
    } else {
        showToast(data.error || 'No matching reservations found', 'error');
        renderBookingsList([]);
    }
}

function renderBookingsList(reservations) {
    elements.bookingsResultsList.innerHTML = '';

    if (!reservations || reservations.length === 0) {
        elements.noBookingsPlaceholder.classList.remove('hidden');
        return;
    }

    elements.noBookingsPlaceholder.classList.add('hidden');

    reservations.forEach(res => {
        const item = document.createElement('div');
        item.className = 'booking-card-item';

        const seats = res.seat_numbers.join(', ');
        const busRoute = res.bus_info ? res.bus_info.route : `Bus ${res.bus_id}`;
        const busName = res.bus_info ? res.bus_info.name : res.bus_id;
        const departure = res.bus_info ? res.bus_info.departure_display : 'Scheduled';
        const bookedOn = res.booking_time_display || res.booking_time;

        item.innerHTML = `
            <div>
                <div style="font-family:monospace; font-weight:800; color:var(--primary); font-size:1rem;">${res.booking_id}</div>
                <div style="font-weight:700; font-size:1.05rem; margin-top:2px;">${res.user.name}</div>
                <div style="font-size:0.85rem; color:var(--text-muted);">${res.user.phone} • ${res.user.email}</div>
                <div style="font-size:0.75rem; color:var(--text-light); margin-top:2px;">Booked: ${bookedOn}</div>
            </div>

            <div>
                <div style="font-weight:700; color:var(--text-main);">${busName}</div>
                <div style="font-size:0.875rem; color:var(--text-muted);">${busRoute}</div>
                <div style="font-size:0.82rem; color:var(--primary); font-weight:700; margin-top:2px;">Departs: ${departure}</div>
            </div>

            <div>
                <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; font-weight:700;">Seats</div>
                <div style="font-weight:700; color:var(--text-main); font-size:0.95rem;">${seats}</div>
                <div style="font-weight:800; color:var(--primary); font-size:1.1rem; margin-top:2px;">₹${res.total_fare.toFixed(2)}</div>
                <span class="badge badge-success" style="margin-top:4px;">${res.payment_status || 'Paid'}</span>
            </div>

            <div style="display:flex; flex-direction:column; gap:0.5rem; align-items:flex-end;">
                <button class="btn btn-secondary btn-sm view-ticket-btn" data-booking-id="${res.booking_id}">
                    View E-Ticket
                </button>
                <button class="btn btn-danger btn-sm open-cancel-btn" data-booking-id="${res.booking_id}">
                    Cancel Seats
                </button>
            </div>
        `;

        elements.bookingsResultsList.appendChild(item);
    });

    document.querySelectorAll('.view-ticket-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const bookingId = btn.getAttribute('data-booking-id');
            const data = await apiCall(`/api/reservations/${bookingId}`);
            if (data.success) {
                renderTicketReceipt(data.reservation, data.reservation.bus_info);
                elements.ticketModal.classList.remove('hidden');
            }
        });
    });

    document.querySelectorAll('.open-cancel-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const bookingId = btn.getAttribute('data-booking-id');
            openCancelModal(bookingId);
        });
    });
}

async function openCancelModal(bookingId) {
    const data = await apiCall(`/api/reservations/${bookingId}`);
    if (!data.success) {
        showToast('Unable to load reservation', 'error');
        return;
    }

    const res = data.reservation;
    state.activeBookingToCancel = res;

    elements.cancelBookingId.textContent = res.booking_id;
    elements.cancelSeatsCheckboxList.innerHTML = '';

    res.seat_numbers.forEach(seatNo => {
        const label = document.createElement('label');
        label.className = 'cancel-seat-option';
        label.innerHTML = `
            <input type="checkbox" value="${seatNo}" checked>
            <span>Seat ${seatNo}</span>
        `;
        elements.cancelSeatsCheckboxList.appendChild(label);
    });

    elements.cancelModal.classList.remove('hidden');
}

async function executeCancellation() {
    if (!state.activeBookingToCancel) return;

    const checkedBoxes = elements.cancelSeatsCheckboxList.querySelectorAll('input:checked');
    if (checkedBoxes.length === 0) {
        showToast('Please select at least one seat to cancel', 'error');
        return;
    }

    const seatsToCancel = Array.from(checkedBoxes).map(cb => parseInt(cb.value));
    const bookingId = state.activeBookingToCancel.booking_id;

    elements.executeCancelBtn.disabled = true;
    elements.executeCancelBtn.textContent = 'Cancelling...';

    const data = await apiCall(`/api/reservations/${bookingId}/cancel`, {
        method: 'POST',
        body: JSON.stringify({ seats: seatsToCancel })
    });

    elements.executeCancelBtn.disabled = false;
    elements.executeCancelBtn.textContent = 'Confirm Cancellation';

    if (data.success) {
        elements.cancelModal.classList.add('hidden');
        showToast(data.message, 'success');
        loadAllBookings();
        fetchBuses();
        loadOccupancyReports();
    } else {
        showToast(data.error || 'Cancellation failed', 'error');
    }
}

// -------------------------------------------------------------
// Occupancy Reports
// -------------------------------------------------------------
async function loadOccupancyReports() {
    const data = await apiCall('/api/reports/all-occupancy');
    if (data.success) {
        renderOccupancyTable(data.reports);
    }
}

function renderOccupancyTable(reports) {
    elements.occupancyTableBody.innerHTML = '';
    const query = elements.occupancyBusSearch.value.trim().toLowerCase();

    const filtered = reports.filter(r => {
        if (!query) return true;
        return r.bus_id.toLowerCase().includes(query) || r.name.toLowerCase().includes(query) || r.route.toLowerCase().includes(query);
    });

    filtered.forEach(rep => {
        const tr = document.createElement('tr');

        tr.innerHTML = `
            <td><strong style="font-family:monospace; color:var(--primary);">${rep.bus_id}</strong></td>
            <td><strong>${rep.name}</strong> <span class="badge ${rep.bus_type.toLowerCase() === 'sleeper' ? 'badge-sleeper' : 'badge-seater'}" style="margin-left:4px;">${rep.bus_type}</span></td>
            <td>${rep.route}</td>
            <td><strong style="color:var(--primary);">${rep.departure_display}</strong></td>
            <td>${rep.total_seats}</td>
            <td><span style="color:var(--danger); font-weight:700;">${rep.reserved_seats_count}</span></td>
            <td><span style="color:var(--success); font-weight:700;">${rep.available_seats_count}</span></td>
            <td>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width: ${rep.occupancy_percentage}%;"></div>
                </div>
                <strong>${rep.occupancy_percentage}%</strong>
            </td>
            <td>
                <button class="btn btn-secondary btn-sm view-bus-seat-btn" data-bus-id="${rep.bus_id}">
                    View Map
                </button>
            </td>
        `;

        elements.occupancyTableBody.appendChild(tr);
    });

    document.querySelectorAll('.view-bus-seat-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const busId = btn.getAttribute('data-bus-id');
            openSeatModal(busId);
        });
    });
}

// -------------------------------------------------------------
// Auth Modal Helpers
// -------------------------------------------------------------
function openAuthModal(noticeMsg = '') {
    if (noticeMsg) showToast(noticeMsg, 'info');
    elements.authModal.classList.remove('hidden');
}

function showSignInTab() {
    elements.toggleSignInBtn.classList.add('active');
    elements.toggleSignUpBtn.classList.remove('active');
    elements.signInForm.classList.remove('hidden');
    elements.signUpForm.classList.add('hidden');
}

function showSignUpTab() {
    elements.toggleSignUpBtn.classList.add('active');
    elements.toggleSignInBtn.classList.remove('active');
    elements.signUpForm.classList.remove('hidden');
    elements.signInForm.classList.add('hidden');
}

// -------------------------------------------------------------
// Setup Event Listeners
// -------------------------------------------------------------
function setupEventListeners() {
    // Auth Toggles & Forms
    elements.openAuthModalBtn.addEventListener('click', () => openAuthModal());
    elements.closeAuthModalBtn.addEventListener('click', () => elements.authModal.classList.add('hidden'));
    elements.toggleSignInBtn.addEventListener('click', showSignInTab);
    elements.toggleSignUpBtn.addEventListener('click', showSignUpTab);
    elements.linkToSignUp.addEventListener('click', (e) => { e.preventDefault(); showSignUpTab(); });
    elements.linkToSignIn.addEventListener('click', (e) => { e.preventDefault(); showSignInTab(); });
    elements.signInForm.addEventListener('submit', handleSignIn);
    elements.signUpForm.addEventListener('submit', handleSignUp);
    elements.logoutBtn.addEventListener('click', handleLogout);

    // Search form
    elements.searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        fetchBuses();
    });

    elements.resetSearchBtn.addEventListener('click', () => {
        elements.searchForm.reset();
        init3DayDateSelector();
        fetchBuses();
    });

    // Swap From and To
    elements.swapLocationsBtn.addEventListener('click', () => {
        const fromVal = elements.fromSelect.value;
        const toVal = elements.toSelect.value;

        let canSwapToFrom = false;
        Array.from(elements.fromSelect.options).forEach(opt => {
            if (opt.value === toVal) canSwapToFrom = true;
        });

        if (canSwapToFrom || !toVal) {
            elements.fromSelect.value = toVal;
            elements.toSelect.value = fromVal;
            fetchBuses();
        } else {
            showToast(`${toVal} is an outstation destination and cannot be selected as Goa origin.`, 'error');
        }
    });

    // Modal Close buttons
    elements.closeSeatModalBtn.addEventListener('click', () => elements.seatModal.classList.add('hidden'));
    elements.closeCheckoutModalBtn.addEventListener('click', () => elements.checkoutModal.classList.add('hidden'));
    elements.closeTicketModalBtn.addEventListener('click', () => elements.ticketModal.classList.add('hidden'));
    elements.doneTicketBtn.addEventListener('click', () => elements.ticketModal.classList.add('hidden'));
    elements.closeCancelModalBtn.addEventListener('click', () => elements.cancelModal.classList.add('hidden'));
    elements.abortCancelBtn.addEventListener('click', () => elements.cancelModal.classList.add('hidden'));

    // Seat Modal -> Checkout
    elements.proceedToCheckoutBtn.addEventListener('click', handleProceedToCheckout);
    elements.backToSeatsBtn.addEventListener('click', () => {
        elements.checkoutModal.classList.add('hidden');
        elements.seatModal.classList.remove('hidden');
    });

    // Form Submit Booking
    elements.passengerForm.addEventListener('submit', handleBookingSubmit);

    // Bookings Search
    elements.searchBookingBtn.addEventListener('click', searchBookings);
    elements.bookingSearchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchBookings();
    });
    elements.loadAllBookingsBtn.addEventListener('click', loadAllBookings);

    // Cancel Execution
    elements.executeCancelBtn.addEventListener('click', executeCancellation);

    // Occupancy Search & Refresh
    elements.occupancyBusSearch.addEventListener('input', () => {
        apiCall('/api/reports/all-occupancy').then(data => {
            if (data.success) renderOccupancyTable(data.reports);
        });
    });
    elements.refreshOccupancyBtn.addEventListener('click', loadOccupancyReports);

    // Close Modals on Backdrop Click
    window.addEventListener('click', (e) => {
        if (e.target === elements.authModal) elements.authModal.classList.add('hidden');
        if (e.target === elements.seatModal) elements.seatModal.classList.add('hidden');
        if (e.target === elements.checkoutModal) elements.checkoutModal.classList.add('hidden');
        if (e.target === elements.ticketModal) elements.ticketModal.classList.add('hidden');
        if (e.target === elements.cancelModal) elements.cancelModal.classList.add('hidden');
    });
}
