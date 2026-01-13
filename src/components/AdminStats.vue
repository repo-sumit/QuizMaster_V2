<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/admin/dashboard">
          <span class="text-primary">Quiz</span>Master
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/stats">Stats</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <button class="btn btn-danger ms-2" @click="logout">
                <i class="fas fa-sign-out-alt"></i> Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid p-5">
      <div class="d-flex flex-wrap align-items-center justify-content-between mb-4">
        <div>
          <div class="d-flex align-items-center gap-2">
            <span class="badge-soft">Live analytics</span>
            <span class="muted small">Last updated {{ lastUpdated }}</span>
          </div>
          <h1 class="h3 mb-1 display-font">Admin Analytics Hub</h1>
          <p class="muted mb-0">Track content growth, student momentum, and performance highlights.</p>
        </div>
        <div class="d-flex gap-2 ms-auto">
          <button class="btn btn-outline-brand" @click="fetchDashboardData">
            <i class="fas fa-rotate"></i> Refresh
          </button>
          <button class="btn btn-primary" @click="exportData">
            <i class="fas fa-file-export"></i> Export
          </button>
        </div>
      </div>

      <div class="row g-4 mb-4">
        <div class="col-xl-2 col-md-6">
          <div class="card border-left-primary h-100 py-2 stat-card">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Subjects</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.subjects_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-book fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-2 col-md-6">
          <div class="card border-left-success h-100 py-2 stat-card">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Chapters</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.chapters_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-folder fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-2 col-md-6">
          <div class="card border-left-info h-100 py-2 stat-card">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Quizzes</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.quizzes_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-question-circle fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-2 col-md-6">
          <div class="card border-left-warning h-100 py-2 stat-card">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Questions</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.questions_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-list fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-2 col-md-6">
          <div class="card border-left-danger h-100 py-2 stat-card">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-danger text-uppercase mb-1">Users</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.users_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-users fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4 mb-4">
        <div class="col-xl-7">
          <div class="card glass-panel p-4 h-100">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <div>
                <h5 class="mb-1 display-font">Content Pulse</h5>
                <p class="muted small mb-0">A quick look at your total content footprint.</p>
              </div>
              <span class="score-chip">Total {{ totalContent }}</span>
            </div>
            <canvas ref="contentChart"></canvas>
          </div>
        </div>
        <div class="col-xl-5">
          <div class="card glass-panel p-4 h-100">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <div>
                <h5 class="mb-1 display-font">Top Performers</h5>
                <p class="muted small mb-0">Highest average scores across students.</p>
              </div>
              <span class="badge-soft">Top 5</span>
            </div>
            <canvas ref="performerChart"></canvas>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-xl-4">
          <div class="card glass-panel p-4 h-100">
            <h5 class="mb-3 display-font">Highlights</h5>
            <div class="d-flex align-items-center justify-content-between mb-3">
              <div>
                <p class="muted small mb-1">Best performer</p>
                <p class="mb-0 fw-semibold">{{ bestPerformer?.full_name || 'No data yet' }}</p>
              </div>
              <span class="score-chip">{{ bestPerformer?.avg_score || 0 }}%</span>
            </div>
            <div class="d-flex align-items-center justify-content-between mb-3">
              <div>
                <p class="muted small mb-1">Most active</p>
                <p class="mb-0 fw-semibold">{{ mostActive?.full_name || 'No data yet' }}</p>
              </div>
              <span class="score-chip">{{ mostActive?.total_attempts || 0 }} attempts</span>
            </div>
            <div class="rounded-4 p-3 bg-white">
              <p class="muted small mb-1">Average score across users</p>
              <p class="h5 mb-0 display-font">{{ averageScore }}%</p>
            </div>
          </div>
        </div>

        <div class="col-xl-8">
          <div class="card shadow mb-4 h-100">
            <div class="card-header py-3 bg-transparent border-0">
              <h6 class="m-0 font-weight-bold text-primary">User Score Summary</h6>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover align-middle">
                  <thead>
                    <tr>
                      <th>Username</th>
                      <th>Full Name</th>
                      <th>Total Attempts</th>
                      <th>Average Score (%)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="summary in score_summary" :key="summary.username">
                      <td>
                        <router-link :to="`/admin/user/${summary.user_id}/scores`" class="text-primary">
                          {{ summary.username }}
                        </router-link>
                      </td>
                      <td>{{ summary.full_name }}</td>
                      <td>{{ summary.total_attempts }}</td>
                      <td>{{ summary.avg_score }}</td>
                    </tr>
                  </tbody>
                </table>
                <div v-if="!score_summary.length" class="text-center muted py-4">
                  No score data available yet.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: 'AdminStats',
  setup() {
    const router = useRouter();
    const stats = ref({ subjects_count: 0, chapters_count: 0, quizzes_count: 0, questions_count: 0, users_count: 0 });
    const score_summary = ref([]);
    const subjects = ref([]);
    const lastUpdated = ref('Just now');
    const contentChart = ref(null);
    const performerChart = ref(null);
    let contentChartInstance = null;
    let performerChartInstance = null;

    const totalContent = computed(() => {
      return stats.value.subjects_count + stats.value.chapters_count + stats.value.quizzes_count + stats.value.questions_count;
    });

    const topPerformers = computed(() => {
      return [...score_summary.value]
        .map(summary => ({
          ...summary,
          avg_score: Number(summary.avg_score) || 0,
          total_attempts: Number(summary.total_attempts) || 0,
        }))
        .sort((a, b) => b.avg_score - a.avg_score)
        .slice(0, 5);
    });

    const bestPerformer = computed(() => topPerformers.value[0] || null);

    const mostActive = computed(() => {
      if (!score_summary.value.length) return null;
      return [...score_summary.value]
        .map(summary => ({
          ...summary,
          total_attempts: Number(summary.total_attempts) || 0,
        }))
        .sort((a, b) => b.total_attempts - a.total_attempts)[0];
    });

    const averageScore = computed(() => {
      if (!score_summary.value.length) return 0;
      const total = score_summary.value.reduce((sum, summary) => sum + (Number(summary.avg_score) || 0), 0);
      return (total / score_summary.value.length).toFixed(1);
    });

    const fetchDashboardData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/dashboard/admin', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const data = await response.json();
          stats.value = data.stats;
          score_summary.value = data.score_summary.map(summary => ({
            ...summary,
            user_id: data.score_summary.find(s => s.username === summary.username)?.user_id || null
          }));
          subjects.value = data.subjects;
          lastUpdated.value = new Date().toLocaleString();
        } else {
          console.error('Failed to fetch dashboard data:', await response.json());
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };

    const exportData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/export', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          alert("Data export in progress. Please check your email.");
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'subjects_export.csv';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        } else {
          console.error('Failed to export data:', await response.json());
        }
      } catch (error) {
        console.error('Error exporting data:', error);
      }
    };

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };

    const buildContentChart = () => {
      if (!contentChart.value) return;
      if (contentChartInstance) {
        contentChartInstance.destroy();
      }
      const labels = ['Subjects', 'Chapters', 'Quizzes', 'Questions'];
      const values = [
        stats.value.subjects_count,
        stats.value.chapters_count,
        stats.value.quizzes_count,
        stats.value.questions_count,
      ];
      contentChartInstance = new Chart(contentChart.value, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Content items',
              data: values,
              backgroundColor: ['#0ea5a4', '#38bdf8', '#f59e0b', '#f97316'],
              borderRadius: 12,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
          },
          scales: {
            y: { beginAtZero: true, ticks: { stepSize: 1 } },
          },
        },
      });
    };

    const buildPerformerChart = () => {
      if (!performerChart.value) return;
      if (performerChartInstance) {
        performerChartInstance.destroy();
      }
      const labels = topPerformers.value.map(item => item.full_name || item.username);
      const values = topPerformers.value.map(item => item.avg_score);
      performerChartInstance = new Chart(performerChart.value, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'Average score',
              data: values,
              borderColor: '#0ea5a4',
              backgroundColor: 'rgba(14, 165, 164, 0.2)',
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            y: { min: 0, max: 100 },
          },
        },
      });
    };

    watch([stats, score_summary], () => {
      buildContentChart();
      buildPerformerChart();
    }, { deep: true });

    onMounted(() => {
      fetchDashboardData();
    });

    onBeforeUnmount(() => {
      if (contentChartInstance) {
        contentChartInstance.destroy();
      }
      if (performerChartInstance) {
        performerChartInstance.destroy();
      }
    });

    return {
      stats,
      score_summary,
      subjects,
      contentChart,
      performerChart,
      lastUpdated,
      totalContent,
      topPerformers,
      bestPerformer,
      mostActive,
      averageScore,
      exportData,
      logout,
      fetchDashboardData,
    };
  },
};
</script>

<style scoped>
.gap-2 {
  gap: 0.5rem;
}

.border-left-primary {
  border-left: 0.25rem solid #4e73df !important;
}

.border-left-success {
  border-left: 0.25rem solid #1cc88a !important;
}

.border-left-info {
  border-left: 0.25rem solid #36b9cc !important;
}

.border-left-warning {
  border-left: 0.25rem solid #f6c23e !important;
}

.border-left-danger {
  border-left: 0.25rem solid #e74a3b !important;
}
</style>
