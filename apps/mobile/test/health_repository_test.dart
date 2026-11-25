import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fitness_ai_mobile/core/errors/app_failure.dart';
import 'package:fitness_ai_mobile/features/health/data/health_dto.dart';
import 'package:fitness_ai_mobile/features/health/data/health_remote_data_source.dart';
import 'package:fitness_ai_mobile/features/health/data/health_repository_impl.dart';

class _MockRemote extends Mock implements HealthRemoteDataSource {}

void main() {
  late _MockRemote remote;
  late HealthRepositoryImpl repository;

  setUp(() {
    remote = _MockRemote();
    repository = HealthRepositoryImpl(remote);
  });

  test('success maps dto to domain', () async {
    when(() => remote.getReady()).thenAnswer(
      (_) async => HealthReadyDto(
        status: 'ready',
        service: 'fitness-ai-backend',
        version: '0.1.0',
        database: 'up',
      ),
    );
    final status = await repository.fetchReadyStatus();
    expect(status.isReady, isTrue);
  });

  test('failure maps connection error', () async {
    when(() => remote.getReady()).thenThrow(
      DioException(
        requestOptions: RequestOptions(path: '/health/ready'),
        type: DioExceptionType.connectionError,
      ),
    );
    expect(
      () => repository.fetchReadyStatus(),
      throwsA(
        isA<AppFailure>().having(
          (f) => f.message,
          'message',
          'Backend unreachable',
        ),
      ),
    );
  });
}
