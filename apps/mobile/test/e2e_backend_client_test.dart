import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('live backend client path', () async {
    final dio = Dio(
      BaseOptions(
        baseUrl: 'http://127.0.0.1:8080',
        connectTimeout: const Duration(seconds: 5),
        receiveTimeout: const Duration(seconds: 10),
      ),
    );
    final live = await dio.get('/health/live');
    expect(live.statusCode, 200);
    final ready = await dio.get('/health/ready');
    expect(ready.statusCode, 200);
    expect(ready.data['checks']['database'], 'up');
  }, tags: ['e2e']);

  test('unreachable backend error path', () async {
    final dio = Dio(
      BaseOptions(
        baseUrl: 'http://127.0.0.1:1',
        connectTimeout: const Duration(seconds: 1),
        receiveTimeout: const Duration(seconds: 1),
      ),
    );
    expect(() => dio.get('/health/ready'), throwsA(isA<DioException>()));
  }, tags: ['e2e']);
}
