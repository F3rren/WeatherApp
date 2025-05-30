"""
Layout Builder for the MeteoApp.
Centralizes layout building functions for different UI components.
"""

import flet as ft

class LayoutBuilder:
    """
    Layout builder class for the MeteoApp.
    Handles the construction of layout components.
    """
    
    @staticmethod
    def build_sidebar_container(sidebar, animation_duration=500, animation_curve=ft.AnimationCurve.EASE_IN_OUT):
        """
        Build the sidebar container.
        
        Args:
            sidebar: La sidebar da inserire nel container
            animation_duration: Duration for animations in milliseconds
            animation_curve: Animation curve type
            
        Returns:
            ft.Container: The sidebar container
        """
        return ft.Container(
            content=sidebar.build(),
            col={"xs": 12},
            margin=10,
            padding=10,
            border_radius=15,
            animate=ft.Animation(animation_duration, animation_curve)
        )
    
    @staticmethod
    def build_content_container(content, col={"xs": 12}, 
                              animation_duration=500, animation_curve=ft.AnimationCurve.EASE_IN_OUT):
        """
        Build a content container with standard styling.
        
        Args:
            content: The content to place in the container
            col: Column specification for the responsive row
            animation_duration: Duration for animations in milliseconds
            animation_curve: Animation curve type
            
        Returns:
            ft.Container: The content container
        """
        return ft.Container(
            content=content,
            col=col,
            margin=10,
            padding=10,
            border_radius=15,
            expand=True,  # <--- ADD THIS LINE
            animate=ft.Animation(animation_duration, animation_curve)
        )
    
    @staticmethod
    def build_main_layout(sidebar_container, info_container_wrapper, 
                        weekly_container_wrapper, chart_container_wrapper,
                        air_pollution_chart_container_wrapper, air_pollution_container_wrapper):
        """
        Build the main application layout.
        
        Args:
            sidebar_container: The container for the sidebar
            info_container_wrapper: The container for weather information
            weekly_container_wrapper: The container for weekly forecast
            chart_container_wrapper: The container for charts
            air_pollution_chart_container_wrapper: The container for air pollution chart
            air_pollution_container_wrapper: The container for air pollution info
            
        Returns:
            ft.ListView: The main layout of the application
        """
        return ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
            controls=[
                ft.ResponsiveRow(
                    controls=[sidebar_container]
                ),
                ft.ResponsiveRow(
                    controls=[info_container_wrapper]
                ),
                ft.ResponsiveRow(
                    controls=[
                        weekly_container_wrapper,
                        chart_container_wrapper
                    ]
                ),
                ft.ResponsiveRow(
                    controls=[
                        air_pollution_chart_container_wrapper,
                        air_pollution_container_wrapper
                    ]
                )
            ]
        )
