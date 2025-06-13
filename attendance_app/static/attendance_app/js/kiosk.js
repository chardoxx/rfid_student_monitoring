// Kiosk Interface Scripts
document.addEventListener('DOMContentLoaded', function() {
    const rfidInput = document.getElementById('rfid-input');
    const studentDisplay = document.getElementById('student-display');
    const studentPhoto = document.getElementById('student-photo');
    const studentName = document.getElementById('student-name');
    const studentId = document.getElementById('student-id');
    const timeIn = document.getElementById('time-in');
    const timeOut = document.getElementById('time-out');
    const instructionText = document.getElementById('instruction-text');
    const rfidAnimation = document.getElementById('rfid-animation');
    
    // Mock data for demonstration
    const students = {
        '123456789': {
            name: 'Juan Dela Cruz',
            id: '2023-00123',
            photo: '../img/placeholder.jpg',
            lastTimeIn: '08:15 AM',
            lastTimeOut: '04:30 PM'
        },
        '987654321': {
            name: 'Maria Santos',
            id: '2023-00456',
            photo: '../img/placeholder.jpg',
            lastTimeIn: '07:50 AM',
            lastTimeOut: '03:45 PM'
        }
    };

    // Simulate RFID input (in real app, this would come from hardware)
    rfidInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const rfidTag = rfidInput.value.trim();
            processRFIDScan(rfidTag);
            rfidInput.value = '';
        }
    });

    // For demo purposes - simulate RFID scan button
    const simulateScanBtn = document.getElementById('simulate-scan');
    if (simulateScanBtn) {
        simulateScanBtn.addEventListener('click', function() {
            const demoTags = Object.keys(students);
            const randomTag = demoTags[Math.floor(Math.random() * demoTags.length)];
            processRFIDScan(randomTag);
        });
    }

    function processRFIDScan(rfidTag) {
        // Show scanning animation
        rfidAnimation.textContent = '⌛';
        instructionText.textContent = 'Processing...';
        
        // Simulate API call delay
        setTimeout(() => {
            const student = students[rfidTag];
            
            if (student) {
                // Display student info
                studentPhoto.src = student.photo;
                studentName.textContent = student.name;
                studentId.textContent = `ID: ${student.id}`;
                timeIn.textContent = student.lastTimeIn;
                timeOut.textContent = student.lastTimeOut;
                
                // Update UI
                studentDisplay.style.display = 'block';
                instructionText.textContent = 'Welcome! Please proceed.';
                rfidAnimation.textContent = '✓';
                rfidAnimation.style.color = '#4CAF50';
                
                // In a real app, send this data to the server
                logAttendance(rfidTag);
                
                // Reset after 5 seconds
                setTimeout(resetKiosk, 5000);
            } else {
                // Invalid RFID tag
                studentDisplay.style.display = 'none';
                instructionText.textContent = 'Invalid RFID tag. Please try again or contact administrator.';
                rfidAnimation.textContent = '✗';
                rfidAnimation.style.color = '#F44336';
                
                // Reset after 3 seconds
                setTimeout(resetKiosk, 3000);
            }
        }, 1000);
    }

    function logAttendance(rfidTag) {
        // In a real app, this would send data to the server
        console.log(`Attendance logged for RFID: ${rfidTag}`);
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        // Determine if this is time in or out
        const isTimeIn = Math.random() > 0.5; // Demo only - real app would have logic
        
        if (isTimeIn) {
            console.log(`Time In at ${timeString}`);
            // Update UI
            timeIn.textContent = timeString;
        } else {
            console.log(`Time Out at ${timeString}`);
            // Update UI
            timeOut.textContent = timeString;
        }
    }

    function resetKiosk() {
        studentDisplay.style.display = 'none';
        instructionText.textContent = 'Please tap your RFID card to log attendance';
        rfidAnimation.textContent = '⌨';
        rfidAnimation.style.color = '#FFC107';
    }

    // Initialize
    resetKiosk();
    
    // In a real implementation, you would have hardware integration:
    // initializeRFIDReader();
});

// RFID Hardware Integration (example)
function initializeRFIDReader() {
    // This would interface with the actual RFID hardware
    // Implementation depends on the specific RFID reader API
    
    console.log("Initializing RFID reader...");
    
    // Example using a hypothetical RFID reader library
    /*
    const reader = new RFID.Reader({
        port: '/dev/ttyUSB0',
        baudRate: 9600
    });
    
    reader.on('tag', function(tag) {
        console.log('RFID tag detected:', tag);
        processRFIDScan(tag.uid);
    });
    
    reader.on('error', function(err) {
        console.error('RFID reader error:', err);
    });
    */
}