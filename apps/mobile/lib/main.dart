import 'package:flutter/material.dart';
import 'package:fitness_ai_mobile/app/app.dart';
import 'package:fitness_ai_mobile/app/dependency_injection/injection.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  configureDependencies();
  runApp(const FitnessAiApp());
}
