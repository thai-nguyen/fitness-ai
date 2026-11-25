import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:fitness_ai_mobile/core/errors/app_failure.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_repository.dart';
import 'package:fitness_ai_mobile/features/health/presentation/cubit/health_state.dart';

class HealthCubit extends Cubit<HealthState> {
  HealthCubit(this._repository) : super(const HealthInitial());

  final HealthRepository _repository;

  Future<void> check() async {
    emit(const HealthLoading());
    try {
      final status = await _repository.fetchReadyStatus();
      emit(HealthSuccess(status));
    } on AppFailure catch (failure) {
      emit(HealthFailureState(failure.message));
    } catch (_) {
      emit(const HealthFailureState('Unexpected error'));
    }
  }
}
