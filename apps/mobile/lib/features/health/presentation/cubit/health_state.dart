import 'package:equatable/equatable.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_status.dart';

sealed class HealthState extends Equatable {
  const HealthState();

  @override
  List<Object?> get props => [];
}

class HealthInitial extends HealthState {
  const HealthInitial();
}

class HealthLoading extends HealthState {
  const HealthLoading();
}

class HealthSuccess extends HealthState {
  const HealthSuccess(this.status);

  final HealthStatus status;

  @override
  List<Object?> get props => [status];
}

class HealthFailureState extends HealthState {
  const HealthFailureState(this.message);

  final String message;

  @override
  List<Object?> get props => [message];
}
