// Pipeline Health Chart (Bar)
const ctxPipeline = document.getElementById('pipelineChart').getContext('2d');
const pipelineChart = new Chart(ctxPipeline, {
    type: 'bar',
    data: {
        labels: ['Applied', 'Screening', 'Interview', 'Offered', 'Hired'],
        datasets: [{
            label: 'Candidates in Pipeline',
            data: [150, 120, 100, 80, 50],
            backgroundColor: 'rgba(52, 152, 219, 0.6)',
            borderColor: 'rgba(52, 152, 219, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Candidate Sourcing Chart (Pie)
const ctxSource = document.getElementById('sourceChart').getContext('2d');
const sourceChart = new Chart(ctxSource, {
    type: 'pie',
    data: {
        labels: ['LinkedIn', 'Job Boards', 'Referrals', 'Social Media', 'Agency'],
        datasets: [{
            label: 'Sourcing Channels',
            data: [200, 150, 100, 50, 25],
            backgroundColor: [
                'rgba(231, 76, 60, 0.6)',
                'rgba(46, 204, 113, 0.6)',
                'rgba(52, 152, 219, 0.6)',
                'rgba(241, 196, 15, 0.6)',
                'rgba(155, 89, 182, 0.6)'
            ],
            borderColor: [
                'rgba(231, 76, 60, 1)',
                'rgba(46, 204, 113, 1)',
                'rgba(52, 152, 219, 1)',
                'rgba(241, 196, 15, 1)',
                'rgba(155, 89, 182, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true
    }
});

// Screening & Interview Chart (Bar)
const ctxScreening = document.getElementById('screeningChart').getContext('2d');
const screeningChart = new Chart(ctxScreening, {
    type: 'bar',
    data: {
        labels: ['Passed Screening', 'Passed Interview'],
        datasets: [{
            label: 'Candidates',
            data: [120, 90],
            backgroundColor: 'rgba(46, 204, 113, 0.6)',
            borderColor: 'rgba(46, 204, 113, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Diversity & Inclusion Chart (Pie)
const ctxDiversity = document.getElementById('diversityChart').getContext('2d');
const diversityChart = new Chart(ctxDiversity, {
    type: 'pie',
    data: {
        labels: ['Male', 'Female', 'Other'],
        datasets: [{
            label: 'Gender Distribution',
            data: [300, 200, 50],
            backgroundColor: [
                'rgba(52, 152, 219, 0.6)',
                'rgba(231, 76, 60, 0.6)',
                'rgba(241, 196, 15, 0.6)'
            ],
            borderColor: [
                'rgba(52, 152, 219, 1)',
                'rgba(231, 76, 60, 1)',
                'rgba(241, 196, 15, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true
    }
});
