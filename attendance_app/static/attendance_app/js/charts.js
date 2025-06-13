// Chart Rendering with Chart.js
class AttendanceCharts {
    constructor() {
        this.charts = {};
        this.attendanceData = {};
        this.filters = {
            dateRange: 'week',
            section: 'all'
        };
        
        this.init();
    }
    
    init() {
        // Initialize all charts on the page
        this.initPieChart();
        this.initLineChart();
        this.initEventListeners();
        
        // Load initial data
        this.loadData();
    }
    
    initPieChart() {
        const ctx = document.getElementById('attendancePieChart');
        if (!ctx) return;
        
        this.charts.pie = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Present', 'Late', 'Absent'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: [
                        '#4CAF50',
                        '#FFC107',
                        '#F44336'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            boxWidth: 12,
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    initLineChart() {
        const ctx = document.getElementById('dailyAttendanceChart');
        if (!ctx) return;
        
        this.charts.line = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Present Students',
                    data: [],
                    borderColor: '#0D47A1',
                    backgroundColor: 'rgba(13, 71, 161, 0.1)',
                    borderWidth: 2,
                    pointBackgroundColor: '#0D47A1',
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Students'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }
    
    initEventListeners() {
        // Date range filter buttons
        document.querySelectorAll('.date-filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.filters.dateRange = btn.dataset.range;
                this.updateActiveFilterButtons();
                this.loadData();
            });
        });
        
        // Section filter dropdown
        const sectionFilter = document.getElementById('section-filter');
        if (sectionFilter) {
            sectionFilter.addEventListener('change', () => {
                this.filters.section = sectionFilter.value;
                this.loadData();
            });
        }
        
        // Window resize event
        window.addEventListener('resize', () => {
            this.resizeCharts();
        });
    }
    
    updateActiveFilterButtons() {
        document.querySelectorAll('.date-filter-btn').forEach(btn => {
            if (btn.dataset.range === this.filters.dateRange) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }
    
    resizeCharts() {
        Object.values(this.charts).forEach(chart => {
            chart.resize();
        });
    }
    
    async loadData() {
        try {
            // Show loading state
            this.showLoading(true);
            
            // In a real app, this would fetch data from your API
            // const response = await fetch(`/api/attendance?range=${this.filters.dateRange}&section=${this.filters.section}`);
            // this.attendanceData = await response.json();
            
            // Mock data for demonstration
            this.attendanceData = this.generateMockData();
            
            // Update charts with new data
            this.updateCharts();
            
        } catch (error) {
            console.error('Error loading attendance data:', error);
        } finally {
            this.showLoading(false);
        }
    }
    
    updateCharts() {
        // Update pie chart
        if (this.charts.pie) {
            this.charts.pie.data.datasets[0].data = [
                this.attendanceData.summary.present,
                this.attendanceData.summary.late,
                this.attendanceData.summary.absent
            ];
            this.charts.pie.update();
        }
        
        // Update line chart
        if (this.charts.line) {
            this.charts.line.data.labels = this.attendanceData.daily.map(day => day.date);
            this.charts.line.data.datasets[0].data = this.attendanceData.daily.map(day => day.present);
            this.charts.line.update();
        }
    }
    
    showLoading(isLoading) {
        const loadingElement = document.getElementById('chart-loading');
        if (loadingElement) {
            loadingElement.style.display = isLoading ? 'block' : 'none';
        }
    }
    
    generateMockData() {
        // Generate mock data based on current filters
        const days = this.filters.dateRange === 'week' ? 7 : 30;
        const basePresent = this.filters.section === 'all' ? 100 : 30;
        
        const dailyData = [];
        for (let i = days; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            
            const dayOfWeek = date.getDay(); // 0 = Sunday, 6 = Saturday
            
            // Fewer students on weekends
            const dayMultiplier = dayOfWeek === 0 || dayOfWeek === 6 ? 0.3 : 1;
            
            // Random variation
            const randomVariation = Math.floor(Math.random() * 20) - 10;
            
            const present = Math.max(10, Math.floor(basePresent * dayMultiplier + randomVariation));
            const late = Math.floor(present * 0.15);
            const absent = Math.floor(present * 0.1);
            
            dailyData.push({
                date: date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }),
                present,
                late,
                absent
            });
        }
        
        // Calculate summary totals
        const summary = dailyData.reduce((acc, day) => {
            acc.present += day.present;
            acc.late += day.late;
            acc.absent += day.absent;
            return acc;
        }, { present: 0, late: 0, absent: 0 });
        
        return {
            summary,
            daily: dailyData
        };
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('attendancePieChart') {
        new AttendanceCharts();
    }
});