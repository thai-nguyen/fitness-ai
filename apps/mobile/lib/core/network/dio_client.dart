import 'package:dio/dio.dart';
import 'package:fitness_ai_mobile/core/config/app_config.dart';

Dio createDio(AppConfig config) {
  return Dio(
    BaseOptions(
      baseUrl: config.apiBaseUrl,
      connectTimeout: config.connectTimeout,
      receiveTimeout: config.receiveTimeout,
      headers: const {'Accept': 'application/json'},
      // Do not log request bodies globally — keep Dio quiet by default.
    ),
  );
}
