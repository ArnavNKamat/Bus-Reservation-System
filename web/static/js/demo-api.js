/* Browser-only API for the GitHub Pages portfolio demo. */
(() => {
    const storageKey = 'goa_express_demo_reservations';
    const customBusesStorageKey = 'goabus_demo_custom_buses';
    const removedBusesStorageKey = 'goabus_demo_removed_buses';
    const adminEmail = 'admin@goabus.demo';
    const adminPassword = 'GoaBusDemo!';
    const towns = [
        'Panaji', 'Mapusa', 'Porvorim', 'Ponda', 'Bicholim', 'Pernem',
        'Calangute', 'Candolim', 'Baga', 'Anjuna', 'Vagator', 'Arambol',
        'Margao', 'Vasco da Gama', 'Canacona', 'Quepem', 'Colva',
        'Benaulim', 'Palolem', 'Agonda', 'Dabolim'
    ];
    const outstation = ['Mumbai', 'Pune', 'Kolhapur', 'Belgaum', 'Bangalore', 'Mangalore', 'Hyderabad'];
    const routes = [
        { source: 'Panaji', destination: 'Margao', name: 'Kadamba Express', fare: 50, type: 'Seater', seats: 40, times: ['06:30', '09:30', '13:30', '18:00'] },
        { source: 'Margao', destination: 'Panaji', name: 'Zuari Link Express', fare: 55, type: 'Seater', seats: 40, times: ['07:00', '10:00', '14:00', '18:30'] },
        { source: 'Panaji', destination: 'Mapusa', name: 'North Goa Shuttle', fare: 40, type: 'Seater', seats: 36, times: ['07:30', '11:00', '15:00', '19:00'] },
        { source: 'Mapusa', destination: 'Panaji', name: 'Capital Connector', fare: 40, type: 'Seater', seats: 36, times: ['08:00', '12:00', '16:00', '20:00'] },
        { source: 'Margao', destination: 'Vasco da Gama', name: 'South Goa Coastal', fare: 45, type: 'Seater', seats: 32, times: ['08:30', '12:30', '17:00'] },
        { source: 'Panaji', destination: 'Mumbai', name: 'Konkan Night Rider', fare: 850, type: 'Sleeper', seats: 32, times: ['17:30', '20:30'] },
        { source: 'Margao', destination: 'Bangalore', name: 'Western Ghats Sleeper', fare: 1100, type: 'Sleeper', seats: 32, times: ['18:00', '21:00'] },
        { source: 'Panaji', destination: 'Pune', name: 'Deccan Express', fare: 700, type: 'Sleeper', seats: 32, times: ['19:00', '21:30'] },
        { source: 'Vasco da Gama', destination: 'Panaji', name: 'Harbour City Link', fare: 45, type: 'Seater', seats: 36, times: ['07:00', '11:30', '16:30'] },
        { source: 'Ponda', destination: 'Margao', name: 'Kadamba South Link', fare: 60, type: 'Seater', seats: 36, times: ['08:00', '13:00', '17:30'] }
    ];

    function readReservations() {
        const stored = localStorage.getItem(storageKey);
        return stored ? JSON.parse(stored) : [];
    }

    function saveReservations(reservations) {
        localStorage.setItem(storageKey, JSON.stringify(reservations));
    }

    function readCustomBuses() {
        const stored = localStorage.getItem(customBusesStorageKey);
        return stored ? JSON.parse(stored) : [];
    }

    function saveCustomBuses(buses) {
        localStorage.setItem(customBusesStorageKey, JSON.stringify(buses));
    }

    function readRemovedBuses() {
        const stored = localStorage.getItem(removedBusesStorageKey);
        return stored ? JSON.parse(stored) : [];
    }

    function isAdmin() {
        const user = JSON.parse(localStorage.getItem('goa_express_user') || 'null');
        return user?.role === 'admin';
    }

    function formatTime(time) {
        const [hours, minutes] = time.split(':').map(Number);
        const suffix = hours >= 12 ? 'PM' : 'AM';
        return `${String(hours % 12 || 12).padStart(2, '0')}:${String(minutes).padStart(2, '0')} ${suffix}`;
    }

    function formatDateTime(date, time) {
        return `${date} ${time}`;
    }

    function makeBus(route, routeIndex, date, time, departureIndex, custom = false) {
        const departure = new Date(`${date}T${time}:00`);
        const durationMinutes = route.type === 'Sleeper' ? 600 : 60 + (routeIndex % 3) * 15;
        const arrival = new Date(departure.getTime() + durationMinutes * 60000);
        const pad = value => String(value).padStart(2, '0');
        const arrivalTime = `${pad(arrival.getHours())}:${pad(arrival.getMinutes())}`;
        const arrivalDate = `${arrival.getFullYear()}-${pad(arrival.getMonth() + 1)}-${pad(arrival.getDate())}`;
        const available = custom ? route.seats : route.seats - (routeIndex * 7 + departureIndex * 3) % 13;
        const bus = {
            bus_id: route.bus_id || `DEMO-${routeIndex + 1}-${date.replaceAll('-', '')}-${departureIndex + 1}`,
            name: route.name,
            source: route.source,
            destination: route.destination,
            route: `${route.source} → ${route.destination}`,
            departure_dt: formatDateTime(date, time),
            arrival_dt: formatDateTime(arrivalDate, arrivalTime),
            departure_display: `${formatTime(time)}, ${date}`,
            arrival_display: `${formatTime(arrivalTime)}, ${arrivalDate}`,
            fare: route.fare,
            bus_type: route.type,
            total_seats: route.seats,
            available_seats_count: available,
            reserved_seats_count: route.seats - available,
            seats: []
        };

        for (let seatNumber = 1; seatNumber <= bus.total_seats; seatNumber++) {
            const isReserved = seatNumber > bus.available_seats_count;
            bus.seats.push({
                seat_number: seatNumber,
                seat_type: seatNumber % 4 === 1 || seatNumber % 4 === 0 ? 'window' : 'aisle',
                is_reserved: isReserved,
                booking_id: ''
            });
        }
        return bus;
    }

    function allBuses() {
        const today = new Date();
        const buses = [];
        for (let day = 0; day < 3; day++) {
            const date = new Date(today);
            date.setDate(today.getDate() + day);
            const dateString = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
            routes.forEach((route, routeIndex) => {
                route.times.forEach((time, departureIndex) => {
                    buses.push(makeBus(route, routeIndex, dateString, time, departureIndex));
                });
            });
        }
        readCustomBuses().forEach((route, routeIndex) => {
            buses.push(makeBus(route, routes.length + routeIndex, route.date, route.time, routeIndex, true));
        });
        const removedBuses = new Set(readRemovedBuses());
        const futureBuses = buses.filter(bus =>
            new Date(bus.departure_dt.replace(' ', 'T')) > new Date() &&
            !removedBuses.has(bus.bus_id)
        );
        const bookings = readReservations();
        futureBuses.forEach(bus => {
            bookings
                .filter(booking => booking.bus_id === bus.bus_id)
                .forEach(booking => {
                    booking.seat_numbers.forEach(seatNumber => {
                        const seat = bus.seats[seatNumber - 1];
                        if (seat && !seat.is_reserved) {
                            seat.is_reserved = true;
                            seat.booking_id = booking.booking_id;
                            bus.available_seats_count--;
                            bus.reserved_seats_count++;
                        }
                    });
                });
        });
        return futureBuses;
    }

    function busSummary(bus) {
        const { seats, ...summary } = bus;
        return summary;
    }

    function busDetails(bus) {
        return { ...bus, seats: bus.seats.map(seat => ({ ...seat })) };
    }

    function reservationsWithBusInfo(reservations, buses) {
        return reservations.map(reservation => {
            const bus = buses.find(item => item.bus_id === reservation.bus_id);
            return {
                ...reservation,
                bus_info: bus ? {
                    name: bus.name,
                    route: bus.route,
                    departure_display: bus.departure_display,
                    arrival_display: bus.arrival_display,
                    bus_type: bus.bus_type
                } : null
            };
        });
    }

    function occupancyFor(bus) {
        const reserved = bus.total_seats - bus.available_seats_count;
        return {
            bus_id: bus.bus_id,
            name: bus.name,
            bus_type: bus.bus_type,
            route: bus.route,
            departure_display: bus.departure_display,
            arrival_display: bus.arrival_display,
            total_seats: bus.total_seats,
            reserved_seats_count: reserved,
            available_seats_count: bus.available_seats_count,
            occupancy_percentage: Math.round(reserved / bus.total_seats * 10000) / 100
        };
    }

    function bodyOf(options) {
        return options.body ? JSON.parse(options.body) : {};
    }

    function json(data) {
        return Promise.resolve(data);
    }

    window.DEMO_MODE = true;
    window.demoApiCall = async (endpoint, options = {}) => {
        const url = new URL(endpoint, window.location.href);
        const method = (options.method || 'GET').toUpperCase();
        const apiPathStart = url.pathname.indexOf('/api/');
        const path = apiPathStart >= 0 ? url.pathname.slice(apiPathStart) : url.pathname;
        const buses = allBuses();

        if (path === '/api/locations') {
            const customBuses = readCustomBuses();
            const unique = values => [...new Map(values.map(value => [value.toLocaleLowerCase(), value])).values()];
            const customSources = customBuses.map(bus => bus.source);
            const customDestinations = customBuses.map(bus => bus.destination);
            return json({
                success: true,
                sources: unique([...towns, ...customSources]),
                destinations: unique([...towns, ...outstation, ...customSources, ...customDestinations]),
                outstation
            });
        }

        if (path === '/api/auth/me') {
            const user = JSON.parse(localStorage.getItem('goa_express_user') || 'null');
            return json({ success: true, authenticated: Boolean(user), user });
        }

        if (path === '/api/auth/signin' && method === 'POST') {
            const input = bodyOf(options);
            const identifier = (input.email_or_phone || '').trim();
            if (!identifier || !input.password) {
                return json({ success: false, error: 'Enter your sign-in details.' });
            }
            if (input.role === 'admin' &&
                (identifier.toLowerCase() !== adminEmail || input.password !== adminPassword)) {
                return json({ success: false, error: 'Administrator demo credentials are incorrect.' });
            }
            if (input.role !== 'admin' && identifier.toLowerCase() === adminEmail) {
                return json({ success: false, error: 'Choose Administrator for the demo admin account.' });
            }
            const user = {
                name: input.role === 'admin' ? 'GoaBus Admin' : identifier.includes('@') ? identifier.split('@')[0] : 'Demo Passenger',
                phone: /^\d+$/.test(identifier) ? identifier : '',
                email: identifier.includes('@') ? identifier : '',
                role: input.role === 'admin' ? 'admin' : 'user'
            };
            localStorage.setItem('goa_express_user', JSON.stringify(user));
            return json({ success: true, user, message: `Welcome, ${user.name}!` });
        }

        if (path === '/api/auth/signup' && method === 'POST') {
            const input = bodyOf(options);
            const user = { name: input.name, phone: input.phone, email: input.email.toLowerCase(), role: 'user' };
            localStorage.setItem('goa_express_user', JSON.stringify(user));
            return json({ success: true, user, message: 'Demo account created.' });
        }

        if (path === '/api/auth/logout' && method === 'POST') {
            localStorage.removeItem('goa_express_user');
            return json({ success: true });
        }

        if (path === '/api/admin/buses' && method === 'GET') {
            if (!isAdmin()) return json({ success: false, error: 'Administrator sign-in is required.' });
            return json({ success: true, buses: buses.map(busSummary) });
        }

        if (path === '/api/buses' && method === 'GET') {
            const filtered = buses.filter(bus =>
                (!url.searchParams.get('source') || bus.source.toLowerCase() === url.searchParams.get('source').toLowerCase()) &&
                (!url.searchParams.get('destination') || bus.destination.toLowerCase() === url.searchParams.get('destination').toLowerCase()) &&
                (!url.searchParams.get('date') || bus.departure_dt.startsWith(url.searchParams.get('date'))) &&
                (!url.searchParams.get('type') || bus.bus_type.toLowerCase() === url.searchParams.get('type').toLowerCase())
            );
            return json({ success: true, count: filtered.length, buses: filtered.map(busSummary) });
        }

        if (path === '/api/buses' && method === 'POST') {
            if (!isAdmin()) return json({ success: false, error: 'Administrator sign-in is required to add buses.' });
            const input = bodyOf(options);
            const name = typeof input.name === 'string' ? input.name.trim() : '';
            const source = typeof input.source === 'string' ? input.source.trim() : '';
            const destination = typeof input.destination === 'string' ? input.destination.trim() : '';
            const seats = Number(input.seats);
            const fare = Number(input.fare);
            const type = input.type;
            const today = new Date();
            const latestDate = new Date(today);
            latestDate.setDate(today.getDate() + 2);
            const dateBounds = value => `${value.getFullYear()}-${String(value.getMonth() + 1).padStart(2, '0')}-${String(value.getDate()).padStart(2, '0')}`;
            const validDate = /^\d{4}-\d{2}-\d{2}$/.test(input.date || '') &&
                input.date >= dateBounds(today) &&
                input.date <= dateBounds(latestDate) &&
                !Number.isNaN(new Date(`${input.date}T00:00:00`).getTime());
            const validTime = /^\d{2}:\d{2}$/.test(input.time || '') &&
                Number(input.time.slice(0, 2)) < 24 &&
                Number(input.time.slice(3, 5)) < 60;
            if (!name || name.length > 60 || !source || source.length > 50 ||
                !destination || destination.length > 50 ||
                source.toLocaleLowerCase() === destination.toLocaleLowerCase() ||
                !validDate || !validTime ||
                new Date(`${input.date}T${input.time}:00`) <= new Date() ||
                !Number.isInteger(seats) || seats < 1 || seats > 60 ||
                !Number.isFinite(fare) || fare <= 0 ||
                !['Seater', 'Sleeper'].includes(type)) {
                return json({ success: false, error: 'Check the bus details. Use a distinct route, a future departure within 3 days, 1–60 seats, and a positive fare.' });
            }

            const customBuses = readCustomBuses();
            const bus = {
                bus_id: `GB-${Date.now().toString(36).toUpperCase()}-${Math.random().toString(36).slice(2, 6).toUpperCase()}`,
                name,
                source,
                destination,
                date: input.date,
                time: input.time,
                fare,
                type,
                seats
            };
            customBuses.push(bus);
            saveCustomBuses(customBuses);
            return json({ success: true, bus });
        }

        const busMatch = path.match(/^\/api\/buses\/([^/]+)$/);
        if (busMatch && method === 'GET') {
            const bus = buses.find(item => item.bus_id === decodeURIComponent(busMatch[1]));
            return json(bus ? { success: true, bus: busDetails(bus) } : { success: false, error: 'Bus not found.' });
        }

        if (busMatch && method === 'DELETE') {
            if (!isAdmin()) return json({ success: false, error: 'Administrator sign-in is required to remove buses.' });
            const busId = decodeURIComponent(busMatch[1]);
            const customBuses = readCustomBuses();
            const index = customBuses.findIndex(bus => bus.bus_id === busId);
            if (index < 0 && !buses.some(bus => bus.bus_id === busId)) {
                return json({ success: false, error: 'Upcoming bus not found.' });
            }
            if (readReservations().some(reservation => reservation.bus_id === busId)) {
                return json({ success: false, error: 'This bus has a demo booking and cannot be removed.' });
            }
            if (index >= 0) {
                customBuses.splice(index, 1);
                saveCustomBuses(customBuses);
            } else {
                const removedBuses = readRemovedBuses();
                removedBuses.push(busId);
                localStorage.setItem(removedBusesStorageKey, JSON.stringify(removedBuses));
            }
            return json({ success: true });
        }

        if (path === '/api/bookings' && method === 'POST') {
            const input = bodyOf(options);
            const bus = buses.find(item => item.bus_id === input.bus_id);
            if (!bus || !input.seats?.length || input.seats.some(seat => bus.seats[seat - 1]?.is_reserved)) {
                return json({ success: false, error: 'That bus or one of those seats is no longer available.' });
            }
            const reservation = {
                booking_id: `DEMO-${Date.now().toString(36).toUpperCase()}`,
                user: { name: input.name, phone: input.phone, email: input.email },
                bus_id: bus.bus_id,
                seat_numbers: input.seats.map(Number),
                booking_time: new Date().toLocaleString(),
                booking_time_display: new Date().toLocaleString(),
                total_fare: input.seats.length * bus.fare,
                payment_mode: 'Demo only',
                payment_status: 'Demo booking — no payment',
                transaction_id: 'NOT-PROCESSED'
            };
            const reservations = readReservations();
            reservations.unshift(reservation);
            saveReservations(reservations);
            return json({
                success: true,
                message: 'Demo booking created. No payment was processed.',
                reservation,
                bus_details: {
                    name: bus.name,
                    route: bus.route,
                    departure_display: bus.departure_display,
                    arrival_display: bus.arrival_display,
                    bus_type: bus.bus_type
                }
            });
        }

        if (path === '/api/reservations' && method === 'GET') {
            const reservations = reservationsWithBusInfo(readReservations(), buses);
            return json({ success: true, count: reservations.length, reservations });
        }

        const reservationMatch = path.match(/^\/api\/reservations\/([^/]+)(?:\/(cancel))?$/);
        if (reservationMatch && method === 'GET') {
            const reservation = readReservations().find(item => item.booking_id === decodeURIComponent(reservationMatch[1]));
            if (!reservation) return json({ success: false, error: 'Booking not found.' });
            return json({
                success: true,
                reservation: reservationsWithBusInfo([reservation], buses)[0]
            });
        }

        if (reservationMatch && reservationMatch[2] === 'cancel' && method === 'POST') {
            const bookingId = decodeURIComponent(reservationMatch[1]);
            const input = bodyOf(options);
            const reservations = readReservations();
            const index = reservations.findIndex(item => item.booking_id === bookingId);
            if (index < 0) return json({ success: false, error: 'Booking not found.' });
            const booking = reservations[index];
            const cancelled = input.seats?.length ? input.seats.map(Number) : [...booking.seat_numbers];
            if (cancelled.some(seat => !booking.seat_numbers.includes(seat))) {
                return json({ success: false, error: 'A selected seat is not part of this booking.' });
            }
            booking.seat_numbers = booking.seat_numbers.filter(seat => !cancelled.includes(seat));
            const bus = buses.find(item => item.bus_id === booking.bus_id);
            booking.total_fare = booking.seat_numbers.length * (bus?.fare || 0);
            const removedCompletely = booking.seat_numbers.length === 0;
            if (removedCompletely) reservations.splice(index, 1);
            saveReservations(reservations);
            return json({
                success: true,
                message: removedCompletely ? 'Demo booking cancelled.' : 'Selected demo seats cancelled.',
                removed_completely: removedCompletely,
                cancelled_seats: cancelled,
                remaining_seats: booking.seat_numbers,
                updated_fare: booking.total_fare
            });
        }

        if (path === '/api/reservations/search' && method === 'GET') {
            const phone = url.searchParams.get('phone') || '';
            const name = (url.searchParams.get('name') || '').toLowerCase();
            const matches = readReservations().filter(reservation =>
                (phone && reservation.user.phone === phone) ||
                (name && reservation.user.name.toLowerCase().includes(name))
            );
            return json({
                success: true,
                count: matches.length,
                reservations: reservationsWithBusInfo(matches, buses)
            });
        }

        if (path === '/api/reports/all-occupancy') {
            if (!isAdmin()) return json({ success: false, error: 'Administrator sign-in is required to view bus analytics.' });
            const reports = buses.map(occupancyFor).sort((left, right) => right.occupancy_percentage - left.occupancy_percentage);
            return json({ success: true, count: reports.length, reports });
        }

        const reportMatch = path.match(/^\/api\/reports\/occupancy\/([^/]+)$/);
        if (reportMatch) {
            if (!isAdmin()) return json({ success: false, error: 'Administrator sign-in is required to view bus analytics.' });
            const bus = buses.find(item => item.bus_id === decodeURIComponent(reportMatch[1]));
            if (!bus) return json({ success: false, error: 'Bus not found.' });
            const report = occupancyFor(bus);
            report.reserved_seats = bus.seats.filter(seat => seat.is_reserved).map(seat => seat.seat_number);
            report.available_seats = bus.seats.filter(seat => !seat.is_reserved).map(seat => seat.seat_number);
            return json({ success: true, report });
        }

        console.error(`Unsupported demo API request: ${method} ${path}`);
        return json({ success: false, error: 'This feature is not available in the portfolio demo.' });
    };
})();
