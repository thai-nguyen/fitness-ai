import 'package:dio/dio.dart';
import 'package:fitness_ai_mobile/core/errors/app_failure.dart';
import 'package:fitness_ai_mobile/features/health/data/health_remote_data_source.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_repository.dart';
import 'package:fitness_ai_mobile/features/health/domain/health_status.dart';

class HealthRepositoryImpl implements HealthRepository {
  HealthRepositoryImpl(this._remote);

  final HealthRemoteDataSource _remote;

  @override
  Future<HealthStatus> fetchReadyStatus() async {
    try {
      final dto = await _remote.getReady();
      return dto.toDomain();
    } on DioException catch (error) {
      final message = _mapDioError(error);
      throw AppFailure(message);
    } catch (_) {
      throw const AppFailure('Unexpected health check failure');
    }
  }

  String _mapDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return 'Backend connection timed out';
      case DioExceptionType.connectionError:
        return 'Backend unreachable';
      case DioExceptionType.badResponse:
        final code = error.response?.statusCode;
        return 'Backend returned HTTP ${code ?? 'error'}';
      default:
        return 'Backend health check failed';
    }
  }
}
