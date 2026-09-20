/**
 * Goa Express - Bus Reservation System Frontend JavaScript
 */

// Application State
const state = {
    locations: { sources: [], destinations: [] },
    buses: [],
    selectedBus: null,
    selectedSeats: new Set(),
    activeBookingToCancel: null
};

// DOM Elements
const elements = {
    // Nav
    navTabs: document.querySelectorAll('.nav-tab'),
    tabPanes: document.querySelectorAll('.tab-pane'),
    
    // Search & Filter
    searchForm: document.getElementById('busSearchForm'),
    fromSelect: document.getElementById('fromSelect'),
    toSelect: document.getElementById('toSelect'),
    dateSelect: document.getElementById('dateSelect'),
    typeFilter: document.getElementById('typeFilter'),
    swapLocationsBtn: document.getElementById('swapLocationsBtn'),
    resetSearchBtn: document.getElementById('resetSearchBtn'),
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
    
    // Checkout Modal
    checkoutModal: document.getElementById('checkoutModal'),
    closeCheckoutModalBtn: document.getElementById('closeCheckoutModalBtn'),
    backToSeatsBtn: document.getElementById('backToSeatsBtn'),
    passengerForm: document.getElementById('passengerForm'),
    checkoutBusName: document.getElementById('checkoutBusName'),
    checkoutBusRoute: document.getElementById('checkoutBusRoute'),
    checkoutSeats: document.getElementById('checkoutSeats'),
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
// Toast Notification
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
            ...options
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`API Error on ${endpoint}:`, error);
        showToast('Network error. Please check your connection.', 'error');
        return { success: false, error: error.message };
    }
}

// -------------------------------------------------------------
// Initialization
// -------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async () => {
    initNavigation();
    initDateInput();
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

function initDateInput() {
    const today = new Date().toISOString().split('T')[0];
    elements.dateSelect.min = today;
}

// -------------------------------------------------------------
// Load Locations (Sources & Destinations)
// -------------------------------------------------------------
async function loadLocations() {
    const data = await apiCall('/api/locations');
    if (data.success) {
        state.locations = data;
        
        // Populate From
        elements.fromSelect.innerHTML = '<option value="">All Goa Towns (Origin)</option>';
        data.sources.forEach(town => {
            const opt = document.createElement('option');
            opt.value = town;
            opt.textContent = town;
            elements.fromSelect.appendChild(opt);
        });

        // Populate To
        elements.toSelect.innerHTML = '<option value="">All Destinations</option>';
        
        // Group Goa towns and outstation
        const goaGroup = document.createElement('optgroup');
        goaGroup.label = 'Goa Local Towns';
        data.sources.forEach(town => {
            const opt = document.createElement('option');
            opt.value = town;
            opt.textContent = town;
            goaGroup.appendChild(opt);
        });
        elements.toSelect.appendChild(goaGroup);

        const outstationGroup = document.createElement('optgroup');
        outstationGroup.label = 'Outstation Cities';
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

    elements.resultsCount.textContent = 'Searching buses...';
    elements.busList.innerHTML = '<div style="text-align:center; padding: 2rem; color: #64748b;">Loading available buses...</div>';

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
    elements.resultsCount.textContent = `${buses.length} bus(es) found`;

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
                    <span class="time-val">${bus.departure_display}</span>
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

    // Attach seat select listeners
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

    // Set Info in Modal Header
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

        // 4 Seats: Col 0, Col 1, [Aisle Gap], Col 2, Col 3
        // Col 0
        const seat1No = r * cols + 1;
        rowDiv.appendChild(createSeatElement(seat1No, seatMap[seat1No], totalSeats));

        // Col 1
        const seat2No = r * cols + 2;
        rowDiv.appendChild(createSeatElement(seat2No, seatMap[seat2No], totalSeats));

        // Walking Aisle Gap
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
        const empty = document.createElement('div');
        return empty;
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
        
        btn.addEventListener('click', () => {
            toggleSeatSelection(seatNo, btn);
        });
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
// Checkout & Passenger Details
// -------------------------------------------------------------
function openCheckoutModal() {
    if (!state.selectedBus || state.selectedSeats.size === 0) return;

    elements.seatModal.classList.add('hidden');
    elements.checkoutModal.classList.remove('hidden');

    const bus = state.selectedBus;
    const selectedArray = Array.from(state.selectedSeats).sort((a, b) => a - b);
    const total = selectedArray.length * bus.fare;

    elements.checkoutBusName.textContent = `${bus.name} (${bus.bus_id})`;
    elements.checkoutBusRoute.textContent = `${bus.source} ➔ ${bus.destination}`;
    elements.checkoutSeats.textContent = selectedArray.join(', ');
    elements.checkoutTotalFare.textContent = `₹${total.toFixed(2)}`;
}

async function handleBookingSubmit(e) {
    e.preventDefault();
    if (!state.selectedBus || state.selectedSeats.size === 0) return;

    const name = document.getElementById('passengerName').value.trim();
    const phone = document.getElementById('passengerPhone').value.trim();
    const email = document.getElementById('passengerEmail').value.trim();

    if (!name || !phone || !email) {
        showToast('Please fill all passenger details', 'error');
        return;
    }

    // Set loading state
    elements.confirmBookingBtn.disabled = true;
    elements.confirmBookingBtnText.textContent = 'Reserving Seats...';

    const payload = {
        bus_id: state.selectedBus.bus_id,
        name: name,
        phone: phone,
        email: email,
        seats: Array.from(state.selectedSeats)
    };

    const data = await apiCall('/api/bookings', {
        method: 'POST',
        body: JSON.stringify(payload)
    });

    elements.confirmBookingBtn.disabled = false;
    elements.confirmBookingBtnText.textContent = 'Confirm & Reserve Seats';

    if (data.success) {
        elements.checkoutModal.classList.add('hidden');
        elements.passengerForm.reset();
        state.selectedSeats.clear();
        
        showToast('Booking Confirmed Successfully!', 'success');
        renderTicketReceipt(data.reservation, data.bus_details);
        elements.ticketModal.classList.remove('hidden');
        
        // Refresh bus data
        fetchBuses();
        loadOccupancyReports();
    } else {
        showToast(data.error || 'Failed to complete booking', 'error');
    }
}

function renderTicketReceipt(reservation, busDetails) {
    const seatsStr = reservation.seat_numbers.join(', ');
    elements.ticketContentArea.innerHTML = `
        <div class="ticket-card">
            <div class="ticket-header">
                <div>
                    <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; opacity:0.8;">Boarding Pass</div>
                    <div class="ticket-booking-id">${reservation.booking_id}</div>
                </div>
                <div style="text-align:right;">
                    <span class="badge badge-success">Confirmed</span>
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
                    <span class="ticket-field-label">Bus Service</span>
                    <span class="ticket-field-val">${busDetails ? busDetails.name : reservation.bus_id}</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Route</span>
                    <span class="ticket-field-val">${busDetails ? busDetails.route : 'Goa Route'}</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Departure</span>
                    <span class="ticket-field-val">${busDetails ? busDetails.departure_display : '--'}</span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Arrival</span>
                    <span class="ticket-field-val">${busDetails ? busDetails.arrival_display : '--'}</span>
                </div>

                <div class="ticket-divider"></div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Booked Seats</span>
                    <span class="ticket-field-val"><strong class="ticket-seats-highlight">${seatsStr}</strong></span>
                </div>

                <div class="ticket-field">
                    <span class="ticket-field-label">Total Amount Paid</span>
                    <span class="ticket-field-val" style="color:var(--primary); font-size:1.2rem;">₹${reservation.total_fare.toFixed(2)}</span>
                </div>

                <div class="ticket-field" style="grid-column:span 2;">
                    <span class="ticket-field-label">Booked On</span>
                    <span class="ticket-field-val" style="font-size:0.85rem; color:#64748b;">${reservation.booking_time}</span>
                </div>
            </div>
        </div>
    `;
}

// -------------------------------------------------------------
// My Bookings & Cancellation
// -------------------------------------------------------------
async function loadAllBookings() {
    elements.bookingsResultsList.innerHTML = '<div style="text-align:center; padding: 2rem; color: #64748b;">Loading reservations...</div>';
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

    elements.bookingsResultsList.innerHTML = '<div style="text-align:center; padding: 2rem; color: #64748b;">Searching...</div>';

    // Check if query is booking ID
    if (query.toUpperCase().startsWith('BKG') || query.toUpperCase().startsWith('PRE')) {
        const data = await apiCall(`/api/reservations/${query}`);
        if (data.success) {
            renderBookingsList([data.reservation]);
            return;
        }
    }

    // Try search by phone or name
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

        item.innerHTML = `
            <div>
                <div style="font-family:monospace; font-weight:800; color:var(--primary); font-size:1rem;">${res.booking_id}</div>
                <div style="font-weight:700; font-size:1.05rem; margin-top:2px;">${res.user.name}</div>
                <div style="font-size:0.85rem; color:var(--text-muted);">${res.user.phone} • ${res.user.email}</div>
            </div>

            <div>
                <div style="font-weight:700; color:var(--text-main);">${busName}</div>
                <div style="font-size:0.875rem; color:var(--text-muted);">${busRoute}</div>
                <div style="font-size:0.8rem; color:var(--text-light); margin-top:2px;">Dep: ${departure}</div>
            </div>

            <div>
                <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase;">Seats</div>
                <div style="font-weight:700; color:var(--text-main); font-size:0.95rem;">${seats}</div>
                <div style="font-weight:800; color:var(--primary); font-size:1.1rem; margin-top:2px;">₹${res.total_fare.toFixed(2)}</div>
            </div>

            <div style="display:flex; flex-direction:column; gap:0.5rem; align-items:flex-end;">
                <button class="btn btn-secondary btn-sm view-ticket-btn" data-booking-id="${res.booking_id}">
                    View Ticket
                </button>
                <button class="btn btn-danger btn-sm open-cancel-btn" data-booking-id="${res.booking_id}">
                    Cancel Seats
                </button>
            </div>
        `;

        elements.bookingsResultsList.appendChild(item);
    });

    // Attach listeners
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
        btn.addEventListener('click', async () => {
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
            <td>${rep.departure_display}</td>
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
// Event Listeners Setup
// -------------------------------------------------------------
function setupEventListeners() {
    // Search form
    elements.searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        fetchBuses();
    });

    elements.resetSearchBtn.addEventListener('click', () => {
        elements.searchForm.reset();
        fetchBuses();
    });

    // Swap From and To
    elements.swapLocationsBtn.addEventListener('click', () => {
        const fromVal = elements.fromSelect.value;
        const toVal = elements.toSelect.value;
        
        // Check if toVal exists in fromSelect
        let canSwapToFrom = false;
        Array.from(elements.fromSelect.options).forEach(opt => {
            if (opt.value === toVal) canSwapToFrom = true;
        });

        if (canSwapToFrom || !toVal) {
            elements.fromSelect.value = toVal;
            elements.toSelect.value = fromVal;
            fetchBuses();
        } else {
            showToast(`${toVal} is an outstation destination and cannot be set as a Goa origin.`, 'error');
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
    elements.proceedToCheckoutBtn.addEventListener('click', openCheckoutModal);
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
        if (e.target === elements.seatModal) elements.seatModal.classList.add('hidden');
        if (e.target === elements.checkoutModal) elements.checkoutModal.classList.add('hidden');
        if (e.target === elements.ticketModal) elements.ticketModal.classList.add('hidden');
        if (e.target === elements.cancelModal) elements.cancelModal.classList.add('hidden');
    });
}
