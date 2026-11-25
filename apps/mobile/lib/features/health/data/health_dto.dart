import 'package:fitness_ai_mobile/features/health/domain/health_status.dart';

class HealthReadyDto {
  HealthReadyDto({
    required this.status,
    required this.service,
    required this.version,
    required this.database,
  });

  final String status;
  final String service;
  final String version;
  final String database;

  factory HealthReadyDto.fromJson(Map<String, dynamic> json) {
    final checks = json['checks'] as Map<String, dynamic>? ?? {};
    return HealthReadyDto(
      status: json['status'] as String? ?? 'unknown',
      service: json['service'] as String? ?? 'unknown',
      version: json['version'] as String? ?? 'unknown',
      database: checks['database'] as String? ?? 'unknown',
    );
  }

  HealthStatus toDomain({DateTime? checkedAt}) {
    return HealthStatus(
      backendStatus: status,
      service: service,
      version: version,
      databaseStatus: database,
      checkedAt: checkedAt ?? DateTime.now(),
    );
  }
}
