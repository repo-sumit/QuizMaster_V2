import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import AdminStats from '../components/AdminStats.vue';
import Dashboard from '../components/Dashboard.vue';
import Subject from '../components/Subject.vue';
import Chapter from '../components/Chapter.vue';
import Quiz from '../components/Quiz.vue';
import UserScores from '../components/UserScores.vue';
import StudentScores from '../views/StudentScores.vue';
import TakeQuiz from '../views/TakeQuiz.vue';
import StudentDashboard from '../views/StudentDashboard.vue';
import StudentChapter from '../views/StudentChapter.vue';
import StudentSubject from '../views/StudentSubject.vue';
import QuizResult from '../views/QuizResult.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin/dashboard', component: Dashboard },
  { path: '/admin/stats', component: AdminStats },
  { path: '/admin/subject/:id', component: Subject },
  { path: '/admin/chapter/:id', component: Chapter },
  { path: '/admin/quiz/:id', component: Quiz },
  { path: '/admin/user/:id/scores', component: UserScores },
  { path: '/user/chapter/:id', component: StudentChapter },
  { path: '/user/dashboard', component: StudentDashboard },
  { path: '/user/subject/:id', component: StudentSubject },
  { path: '/user/quiz/:id', component: TakeQuiz },
  { path: '/user/quiz/:id/results/:score_id', component: QuizResult },
  { path: '/user/scores', component: StudentScores },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;