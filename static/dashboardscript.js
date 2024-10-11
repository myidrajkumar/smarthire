document.addEventListener('DOMContentLoaded', function () {
    // Fetch KPIs
    fetch('https://smarthire-hvsy.onrender.com/analytics/kpis')
        .then(response => response.json())
        .then(data => data.data)
        .then(data => {
            document.getElementById('total-open-positions').textContent = data.total_open_positions;
            document.getElementById('total-candidates-sourced').textContent = data.total_candidates_sourced;
            document.getElementById('offer-acceptance-rate').textContent = data.offer_acceptance_rate + '%';
        })
        .catch(error => console.error('Error fetching KPIs:', error));

    // Function to fetch and populate the job options dynamically
    function fetchJobs() {
        fetch('https://smarthire-hvsy.onrender.com/api/jobs')  // Assuming this API returns a list of jobs
            .then(response => response.json())
            .then(data => data.data)
            .then(data => {
                const jobSelect = document.getElementById('job-select');
                // Clear existing options (if any)
                jobSelect.innerHTML = '<option value="">Select a Job</option>';

                // Populate dropdown with job options
                data.jobs.forEach(job => {
                    const option = document.createElement('option');
                    option.value = job.job_id;
                    option.textContent = `${job.job_title} (ID: ${job.job_id})`;
                    jobSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching jobs:', error));
    }

        // Function to fetch job-specific analytics based on selected job ID
        function fetchJobAnalytics(jobId) {
            if (!jobId) return;  // No job selected, exit the function
    
            fetch(`https://smarthire-hvsy.onrender.com/analytics/jobs/${jobId}`)
                .then(response => response.json())
                .then(data => data.data)
                .then(data => {
                    
                    const pipelineLabels = Object.keys(data.pipeline_health);
                    const pipelineCounts = Object.values(data.pipeline_health);
    
                    const ctxPipeline = document.getElementById('pipelineChart').getContext('2d');

                    // Update the pipeline chart with data for the selected job
                    new Chart(ctxPipeline, {
                        type: 'bar',
                        data: {
                            labels: pipelineLabels,
                            datasets: [{
                                label: 'Candidates in Pipeline',
                                data: pipelineCounts,
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
                })
                .catch(error => console.error('Error fetching job analytics:', error));
        }

            // Event listener for the job select dropdown
    document.getElementById('job-select').addEventListener('change', function () {
        const selectedJobId = this.value;
        fetchJobAnalytics(selectedJobId);  // Fetch and display analytics for the selected job
    });

        // Fetch and populate job options on page load
        fetchJobs();

    // Fetch Sourcing Analytics
    fetch('https://smarthire-hvsy.onrender.com/analytics/sourcing')
    .then(response => response.json())
    .then(data => data.data)  // Access the `data` object from the response
    .then(data => {
        // Extract labels and counts from the `source_breakdown` object
        get_source_breakdown(data);
        // Cost per source
        get_cost_per_source(data);
        // geographical
        get_geographical_source(data);
    })
    .catch(error => console.error('Error fetching sourcing analytics:', error));



    
    // Fetch Screening & Interview Analytics
    fetch('https://smarthire-hvsy.onrender.com/analytics/screeninginterview')
        .then(response => response.json())
        .then(data => data.data)
        .then(data => {
            const screeningLabels = ['Passed Screening', 'Passed Interview'];
            const screeningCounts = [data.passed_screening, data.interview_conversion_rate];

            const ctxScreening = document.getElementById('screeningChart').getContext('2d');
            new Chart(ctxScreening, {
                type: 'bar',
                data: {
                    labels: screeningLabels,
                    datasets: [{
                        label: 'Candidates',
                        data: screeningCounts,
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
        })
        .catch(error => console.error('Error fetching screening analytics:', error));

    // Fetch Diversity & Inclusion Metrics
    fetch('https://smarthire-hvsy.onrender.com/analytics/diversity')
        .then(response => response.json())
        .then(data => data.data)
        .then(data => {
            const genderLabels = Object.keys(data.gender_diversity);
            const genderCounts = Object.values(data.gender_diversity);

            const ctxDiversity = document.getElementById('diversityChart').getContext('2d');
            new Chart(ctxDiversity, {
                type: 'pie',
                data: {
                    labels: genderLabels,
                    datasets: [{
                        label: 'Gender Distribution',
                        data: genderCounts,
                        backgroundColor: [
                            'rgba(52, 152, 219, 0.6)',
                            'rgba(231, 76, 60, 0.6)'
                        ]
                    }]
                },
                options: {
                    responsive: true
                }
            });
        })
        .catch(error => console.error('Error fetching diversity metrics:', error));

// Fetch Compliance Metrics
fetch('https://smarthire-hvsy.onrender.com/analytics/compliance')
    .then(response => response.json())
    .then(data => data.data)  // Access the `data` object from the response
    .then(data => {
        // Update GDPR compliance rate
        document.getElementById('gdpr-compliance-rate').textContent = data.gdpr_compliance_rate.toFixed(2) + '%';

        // Process and display gender distribution
        const genderDistLabels = Object.keys(data.gender_distribution);  // Get gender labels (e.g., Male, Female)
        const genderDistCounts = Object.values(data.gender_distribution);  // Get the counts for each gender

        const genderDistText = genderDistLabels.map((gender, index) => `${gender}: ${genderDistCounts[index]}`).join(', ');
        document.getElementById('gender-distribution').textContent = genderDistText;

        // Process and display ethnicity distribution
        const ethnicityDistLabels = Object.keys(data.ethnicity_distribution);  // Get ethnicity labels (e.g., Caucasian, Asian, etc.)
        const ethnicityDistCounts = Object.values(data.ethnicity_distribution);  // Get the counts for each ethnicity

        const ethnicityDistText = ethnicityDistLabels.map((ethnicity, index) => `${ethnicity}: ${ethnicityDistCounts[index]}`).join(', ');
        document.getElementById('ethnicity-distribution').textContent = ethnicityDistText;
    })
    .catch(error => console.error('Error fetching compliance metrics:', error));


    // Fetch Recruitment Efficiency (Recruiter Performance & Task Completion Rate)
fetch('https://smarthire-hvsy.onrender.com/analytics/efficiency')
.then(response => response.json())
.then(data => data.data)  // Access the `data` object from the response
.then(data => {
    // Recruiter Performance Chart
    const recruiterLabels = Object.keys(data.recruiter_performance);  // Get recruiter names (e.g., John Doe, Jane Smith)
    const recruiterCounts = Object.values(data.recruiter_performance);  // Get applications handled for each recruiter

    const ctxRecruiterPerformance = document.getElementById('recruiterPerformanceChart').getContext('2d');
    new Chart(ctxRecruiterPerformance, {
        type: 'bar',
        data: {
            labels: recruiterLabels,
            datasets: [{
                label: 'Applications Handled',
                data: recruiterCounts,
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

    // Task Completion Rate Table
    const taskCompletionTable = document.querySelector('#task-completion-table tbody');
    const taskCompletionRateKeys = Object.keys(data.task_completion_rate);  // Recruiter names for task completion rates
    const taskCompletionRateValues = Object.values(data.task_completion_rate);  // Task completion rates

    taskCompletionTable.innerHTML = '';  // Clear any existing rows
    taskCompletionRateKeys.forEach((recruiterName, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${recruiterName}</td><td>${taskCompletionRateValues[index].toFixed(2)}%</td>`;
        taskCompletionTable.appendChild(row);
    });
})
.catch(error => console.error('Error fetching recruiter performance:', error));


    // Fetch Candidate Experience & Feedback
// Fetch Candidate Experience & Feedback
fetch('https://smarthire-hvsy.onrender.com/analytics/candidateexperience')
    .then(response => response.json())
    .then(data => data.data)  // Access the `data` object from the response
    .then(data => {
        // Display Average NPS
        document.getElementById('average-nps').textContent = data.average_nps.toFixed(2);

        // If there is no recent feedback in the response, just remove the feedback section
        const feedbackContainer = document.getElementById('recent-feedback');
        feedbackContainer.innerHTML = '<p>No recent feedback available.</p>';
    })
    .catch(error => console.error('Error fetching candidate feedback:', error));


    // Fetch Offer & Hiring Analytics
    fetch('https://smarthire-hvsy.onrender.com/analytics/offers')
        .then(response => response.json())
        .then(data => data.data)
        .then(data => {
            // Offer to Hire Ratio (Gauge Chart)
            const ctxOfferHireRatio = document.getElementById('offerHireRatioChart').getContext('2d');
            new Chart(ctxOfferHireRatio, {
                type: 'doughnut',
                data: {
                    labels: ['Offers Accepted', 'Offers Rejected'],
                    datasets: [{
                        data: [data.offer_to_hire_ratio, 100 - data.offer_to_hire_ratio],
                        backgroundColor: ['#2ecc71', '#e74c3c']
                    }]
                },
                options: {
                    responsive: true,
                    cutout: '70%',
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.label + ': ' + context.raw.toFixed(2) + '%';
                                }
                            }
                        }
                    }
                }
            });

            // Candidate Drop-Off Rate
            document.getElementById('candidate-drop-off-rate').textContent = data.candidate_drop_off_rate.toFixed(2) + '%';
        })
        .catch(error => console.error('Error fetching offer and hiring analytics:', error));
});

function get_source_breakdown(data) {
    const sourceLabels = Object.keys(data.source_breakdown); // Get the sourcing labels (Agency, LinkedIn, etc.)
    const sourceCounts = Object.values(data.source_breakdown); // Get the counts for each source

    const ctxSource = document.getElementById('sourceChart').getContext('2d');
    new Chart(ctxSource, {
        type: 'pie',
        data: {
            labels: sourceLabels,
            datasets: [{
                label: 'Candidates by Source',
                data: sourceCounts,
                backgroundColor: [
                    'rgba(231, 76, 60, 0.6)',
                    'rgba(46, 204, 113, 0.6)',
                    'rgba(52, 152, 219, 0.6)',
                    'rgba(241, 196, 15, 0.6)',
                    'rgba(155, 89, 182, 0.6)'
                ]
            }]
        },
        options: {
            responsive: true
        }
    });
}

function get_cost_per_source(data) {
        // Cost per source data
        const costSourceLabels = Object.keys(data.cost_per_source);  // e.g., LinkedIn, Referral, etc.
        const costSourceValues = Object.values(data.cost_per_source);  // The cost associated with each source

        const ctxCostSource = document.getElementById('costPerSourceChart').getContext('2d');
        new Chart(ctxCostSource, {
            type: 'bar',
            data: {
                labels: costSourceLabels,
                datasets: [{
                    label: 'Cost per Source (USD)',
                    data: costSourceValues,
                    backgroundColor: 'rgba(52, 152, 219, 0.6)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Cost (USD)'  // Label for y-axis
                        }
                    }
                }
            }
        });
}

function get_geographical_source(data) {
       // Geographical sourcing data
       const geoLabels = Object.keys(data.geographical_sourcing);  // e.g., New York, California, etc.
       const geoCounts = Object.values(data.geographical_sourcing);  // Number of candidates from each region

       const ctxGeoSource = document.getElementById('geoSourcingChart').getContext('2d');
       new Chart(ctxGeoSource, {
           type: 'pie',
           data: {
               labels: geoLabels,
               datasets: [{
                   label: 'Candidates by Geography',
                   data: geoCounts,
                   backgroundColor: [
                       'rgba(231, 76, 60, 0.6)',
                       'rgba(46, 204, 113, 0.6)',
                       'rgba(52, 152, 219, 0.6)',
                       'rgba(241, 196, 15, 0.6)',
                       'rgba(155, 89, 182, 0.6)',
                       'rgba(39, 174, 96, 0.6)',
                       'rgba(41, 128, 185, 0.6)'
                   ]
               }]
           },
           options: {
               responsive: true
           }
       });
}
