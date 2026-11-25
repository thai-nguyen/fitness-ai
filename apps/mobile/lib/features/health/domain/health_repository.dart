import 'package:fitness_ai_mobile/features/health/domain/health_status.dart';

abstract class HealthRepository {
  Future<HealthStatus> fetchReadyStatus();
}
