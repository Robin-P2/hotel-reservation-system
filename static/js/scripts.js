document.addEventListener('DOMContentLoaded', function () {
    const checkInInput = document.getElementById('check_in');
    const checkOutInput = document.getElementById('check_out');
    const roomTypeSelect = document.getElementById('room_type');
    const guestNameInput = document.querySelector('input[name="guest_name"]');
    const adultsInput = document.querySelector('input[name="adults"]');
    const childrenInput = document.querySelector('input[name="children"]');
    const totalField = document.getElementById('total_price');
    const roomPriceField = document.getElementById('room_price');
    const form = document.querySelector('form');

    const roomPrices = {
        'Deluxe': 2000,
        'Suite': 4000,
        'Luxury': 6000
    };

    function calculateTotal() {
        const checkInDate = new Date(checkInInput.value);
        const checkOutDate = new Date(checkOutInput.value);
        const roomType = roomTypeSelect.value;
        const pricePerNight = roomPrices[roomType] || 0;

        roomPriceField.textContent = `Room Price per Night: ₹${pricePerNight}`;

        if (!isNaN(checkInDate) && !isNaN(checkOutDate)) {
            const nights = (checkOutDate - checkInDate) / (1000 * 60 * 60 * 24);
            if (nights > 0) {
                const total = pricePerNight * nights;
                totalField.textContent = `₹${total}`;
                return { nights, total, pricePerNight };
            }
        }
        totalField.textContent = '';
        return null;
    }

    checkInInput.addEventListener('change', calculateTotal);
    checkOutInput.addEventListener('change', calculateTotal);
    roomTypeSelect.addEventListener('change', calculateTotal);

    // Auto-select room type if passed via URL (case-insensitive match)
    const urlParams = new URLSearchParams(window.location.search);
    const selectedRoom = urlParams.get('room');
    if (selectedRoom) {
        const matchOption = Array.from(roomTypeSelect.options).find(
            option => option.value.toLowerCase() === selectedRoom.toLowerCase()
        );
        if (matchOption) {
            roomTypeSelect.value = matchOption.value;
            calculateTotal();
        }
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const totals = calculateTotal();
        if (!totals) {
            alert("Please select valid dates and room type.");
            return;
        }

        const name = guestNameInput.value || "Guest";
        const room = roomTypeSelect.value;
        const checkIn = checkInInput.value;
        const checkOut = checkOutInput.value;
        const adults = adultsInput.value || 1;
        const children = childrenInput.value || 0;

        const confirmation = confirm(
            `Please confirm your booking:\n\n` +
            `Name: ${name}\n` +
            `Room: ${room}\n` +
            `Check-in: ${checkIn}\n` +
            `Check-out: ${checkOut}\n` +
            `Adults: ${adults}\n` +
            `Children: ${children}\n` +
            `Room Price per Night: ₹${totals.pricePerNight}\n` +
            `Total Nights: ${totals.nights}\n` +
            `Total Price: ₹${totals.total}`
        );

        if (confirmation) {
            form.submit();
        }
    });
});
