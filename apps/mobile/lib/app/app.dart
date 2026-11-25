import 'package:flutter/material.dart';
import 'package:fitness_ai_mobile/app/router/app_router.dart';

class FitnessAiApp extends StatelessWidget {
  const FitnessAiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Fitness AI',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1B5E20)),
        useMaterial3: true,
      ),
      routerConfig: createAppRouter(),
    );
  }
}
