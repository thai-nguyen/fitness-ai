import 'package:equatable/equatable.dart';

class HealthStatus extends Equatable {
  const HealthStatus({
    required this.backendStatus,
    required this.service,
    required this.version,
    required this.databaseStatus,
    this.checkedAt,
  });

  final String backendStatus;
  final String service;
  final String version;
  final String databaseStatus;
  final DateTime? checkedAt;

  bool get isReady =>
      backendStatus == 'ready' && databaseStatus.toLowerCase() == 'up';

  @override
  List<Object?> get props => [
    backendStatus,
    service,
    version,
    databaseStatus,
    checkedAt,
  ];
}
