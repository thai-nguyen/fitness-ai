import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fitness_ai_mobile/app/dependency_injection/injection.dart';
import 'package:fitness_ai_mobile/core/config/app_config.dart';
import 'package:fitness_ai_mobile/core/errors/app_failure.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_repository.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_status.dart';
import 'package:fitness_ai_mobile/features/health/presentation/cubit/health_cubit.dart';
import 'package:fitness_ai_mobile/features/health/presentation/health_page.dart';

class _MockRepo extends Mock implements HealthRepository {}

void main() {
  late _MockRepo repository;

  setUp(() {
    resetDependencies();
    repository = _MockRepo();
    getIt.registerSingleton<AppConfig>(
      const AppConfig(
        appName: 'Fitness AI',
        apiBaseUrl: 'http://127.0.0.1:8080',
      ),
    );
    getIt.registerFactory<HealthCubit>(() => HealthCubit(repository));
  });

  tearDown(resetDependencies);

  testWidgets('shows error then success after retry', (tester) async {
    var calls = 0;
    when(() => repository.fetchReadyStatus()).thenAnswer((_) async {
      calls += 1;
      await Future<void>.delayed(const Duration(milliseconds: 20));
      if (calls == 1) {
        throw const AppFailure('Backend unreachable');
      }
      return HealthStatus(
        backendStatus: 'ready',
        service: 'fitness-ai-backend',
        version: '0.1.0',
        databaseStatus: 'up',
        checkedAt: DateTime.utc(2026, 11, 25),
      );
    });

    await tester.pumpWidget(const MaterialApp(home: HealthPage()));
    await tester.pump();
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    await tester.pumpAndSettle();
    expect(find.textContaining('unavailable'), findsOneWidget);
    expect(find.text('Backend unreachable'), findsOneWidget);

    await tester.tap(find.text('Retry'));
    await tester.pump();
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
    await tester.pumpAndSettle();
    expect(find.textContaining('fitness-ai-backend'), findsWidgets);
    expect(find.textContaining('Database: up'), findsOneWidget);
  });
}
