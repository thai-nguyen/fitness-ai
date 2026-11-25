import 'package:dio/dio.dart';
import 'package:fitness_ai_mobile/features/health/data/health_dto.dart';

class HealthRemoteDataSource {
  HealthRemoteDataSource(this._dio);

  final Dio _dio;

  Future<HealthReadyDto> getReady() async {
    final response = await _dio.get<Map<String, dynamic>>('/health/ready');
    final data = response.data;
    if (data == null) {
      throw DioException(
        requestOptions: response.requestOptions,
        message: 'Empty readiness response',
      );
    }
    return HealthReadyDto.fromJson(data);
  }
}
