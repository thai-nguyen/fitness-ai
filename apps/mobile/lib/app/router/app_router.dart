import 'package:go_router/go_router.dart';
import 'package:fitness_ai_mobile/features/health/presentation/health_page.dart';

GoRouter createAppRouter() {
  return GoRouter(
    initialLocation: '/health',
    routes: [
      GoRoute(path: '/health', builder: (context, state) => const HealthPage()),
    ],
  );
}
