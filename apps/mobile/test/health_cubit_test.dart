import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fitness_ai_mobile/core/errors/app_failure.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_repository.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_status.dart';
import 'package:fitness_ai_mobile/features/health/presentation/cubit/health_cubit.dart';
import 'package:fitness_ai_mobile/features/health/presentation/cubit/health_state.dart';

class _MockRepo extends Mock implements HealthRepository {}

void main() {
  late _MockRepo repository;

  setUp(() {
    repository = _MockRepo();
  });

  blocTest<HealthCubit, HealthState>(
    'emits loading then success',
    build: () {
      when(() => repository.fetchReadyStatus()).thenAnswer(
        (_) async => const HealthStatus(
          backendStatus: 'ready',
          service: 'fitness-ai-backend',
          version: '0.1.0',
          databaseStatus: 'up',
        ),
      );
      return HealthCubit(repository);
    },
    act: (cubit) => cubit.check(),
    expect: () => [const HealthLoading(), isA<HealthSuccess>()],
  );

  blocTest<HealthCubit, HealthState>(
    'emits loading then failure and retry can succeed',
    build: () {
      var calls = 0;
      when(() => repository.fetchReadyStatus()).thenAnswer((_) async {
        calls += 1;
        if (calls == 1) {
          throw const AppFailure('Backend unreachable');
        }
        return const HealthStatus(
          backendStatus: 'ready',
          service: 'fitness-ai-backend',
          version: '0.1.0',
          databaseStatus: 'up',
        );
      });
      return HealthCubit(repository);
    },
    act: (cubit) async {
      await cubit.check();
      await cubit.check();
    },
    expect: () => [
      const HealthLoading(),
      const HealthFailureState('Backend unreachable'),
      const HealthLoading(),
      isA<HealthSuccess>(),
    ],
  );
}
