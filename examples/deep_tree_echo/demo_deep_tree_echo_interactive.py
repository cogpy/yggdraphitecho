#!/usr/bin/env python3.11
"""
Interactive Demo for Deep Tree Echo FastAPI Endpoints
Showcases all features with live examples and performance metrics
"""
import asyncio
import httpx
import json
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.markdown import Markdown


console = Console()


class DeepTreeEchoDemo:
    """Interactive demonstration of Deep Tree Echo capabilities"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url, timeout=30.0)
    
    def print_header(self, title: str):
        """Print formatted header"""
        console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
        console.print(f"[bold yellow]{title.center(70)}[/bold yellow]")
        console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")
    
    def print_response(self, response: dict, title: str = "Response"):
        """Print formatted JSON response"""
        syntax = Syntax(json.dumps(response, indent=2), "json", theme="monokai")
        console.print(Panel(syntax, title=f"[bold green]{title}[/bold green]", border_style="green"))
    
    def demo_health_check(self):
        """Demonstrate health check endpoint"""
        self.print_header("1. Health Check")
        console.print("[cyan]Testing service health...[/cyan]")
        
        response = self.client.get("/health")
        self.print_response(response.json(), "Health Status")
        
        console.print(f"[green]✓ Service is {'healthy' if response.status_code == 200 else 'unhealthy'}[/green]")
    
    def demo_service_info(self):
        """Demonstrate service information endpoint"""
        self.print_header("2. Service Information")
        console.print("[cyan]Retrieving service information...[/cyan]")
        
        response = self.client.get("/deep_tree_echo/")
        self.print_response(response.json(), "Service Info")
    
    def demo_basic_processing(self):
        """Demonstrate basic DTESN processing"""
        self.print_header("3. Basic DTESN Processing")
        console.print("[cyan]Processing input through Deep Tree Echo State Network...[/cyan]")
        
        request_data = {
            "input_data": "The quick brown fox jumps over the lazy dog",
            "membrane_depth": 4,
            "esn_size": 512,
            "output_format": "json"
        }
        
        console.print("\n[yellow]Request:[/yellow]")
        self.print_response(request_data, "DTESN Request")
        
        start_time = time.time()
        response = self.client.post("/deep_tree_echo/process", json=request_data)
        elapsed = (time.time() - start_time) * 1000
        
        result = response.json()
        self.print_response(result, "DTESN Response")
        
        # Display performance metrics
        if "performance_metrics" in result:
            metrics = result["performance_metrics"]
            table = Table(title="Performance Metrics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Total Processing Time", f"{metrics.get('total_processing_time_ms', 0):.2f} ms")
            table.add_row("DTESN Processing Time", f"{metrics.get('dtesn_processing_time_ms', 0):.2f} ms")
            table.add_row("Overhead", f"{metrics.get('overhead_ms', 0):.2f} ms")
            table.add_row("Round Trip Time", f"{elapsed:.2f} ms")
            
            console.print(table)
    
    def demo_batch_processing(self):
        """Demonstrate batch processing"""
        self.print_header("4. Batch Processing")
        console.print("[cyan]Processing multiple inputs in parallel...[/cyan]")
        
        request_data = {
            "inputs": [
                "First input for batch processing",
                "Second input with different content",
                "Third input to demonstrate parallelism",
                "Fourth input for comprehensive testing",
                "Fifth input completing the batch"
            ],
            "membrane_depth": 3,
            "esn_size": 256,
            "parallel_processing": True,
            "max_batch_size": 10
        }
        
        console.print("\n[yellow]Batch Request (5 inputs):[/yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Processing batch...", total=None)
            
            start_time = time.time()
            response = self.client.post("/deep_tree_echo/batch_process", json=request_data)
            elapsed = (time.time() - start_time) * 1000
            
            progress.update(task, completed=True)
        
        result = response.json()
        
        # Display batch summary
        table = Table(title="Batch Processing Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Inputs", str(len(request_data["inputs"])))
        table.add_row("Successful", str(result.get("successful_count", 0)))
        table.add_row("Failed", str(result.get("failed_count", 0)))
        table.add_row("Total Time", f"{elapsed:.2f} ms")
        table.add_row("Avg Time per Input", f"{elapsed / len(request_data['inputs']):.2f} ms")
        table.add_row("Processing Mode", "Parallel" if request_data["parallel_processing"] else "Sequential")
        
        console.print(table)
        
        console.print("\n[yellow]Sample Results (first 2):[/yellow]")
        for i, res in enumerate(result.get("results", [])[:2]):
            self.print_response(res, f"Result {i+1}")
    
    def demo_streaming(self):
        """Demonstrate streaming processing"""
        self.print_header("5. Streaming Processing")
        console.print("[cyan]Streaming real-time processing updates...[/cyan]")
        
        request_data = {
            "input_data": "Streaming demonstration with real-time updates",
            "membrane_depth": 3,
            "esn_size": 256
        }
        
        try:
            with self.client.stream("POST", "/deep_tree_echo/stream_process", json=request_data) as response:
                console.print(f"[green]Stream started (Status: {response.status_code})[/green]")
                
                event_count = 0
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        event_count += 1
                        data = json.loads(line[6:])
                        console.print(f"[yellow]Event {event_count}:[/yellow] {data.get('status', 'unknown')}")
                        
                        if event_count >= 3:  # Limit display
                            console.print("[dim]... (stream continues)[/dim]")
                            break
        except Exception as e:
            console.print(f"[yellow]Note: Streaming may not be fully implemented yet: {e}[/yellow]")
            console.print("[cyan]Falling back to standard processing...[/cyan]")
            response = self.client.post("/deep_tree_echo/process", json=request_data)
            if response.status_code == 200:
                console.print("[green]✓ Standard processing successful[/green]")
    
    def demo_system_status(self):
        """Demonstrate system status endpoints"""
        self.print_header("6. System Status & Information")
        
        # Main status
        console.print("[cyan]1. System Status:[/cyan]")
        response = self.client.get("/deep_tree_echo/status")
        self.print_response(response.json(), "System Status")
        
        # Membrane info
        console.print("\n[cyan]2. Membrane System Information:[/cyan]")
        response = self.client.get("/deep_tree_echo/membrane_info")
        self.print_response(response.json(), "Membrane Info")
        
        # ESN state
        console.print("\n[cyan]3. Echo State Network Information:[/cyan]")
        response = self.client.get("/deep_tree_echo/esn_state")
        self.print_response(response.json(), "ESN State")
        
        # Engine integration
        console.print("\n[cyan]4. Engine Integration Status:[/cyan]")
        response = self.client.get("/deep_tree_echo/engine_integration")
        self.print_response(response.json(), "Engine Integration")
    
    def demo_performance_metrics(self):
        """Demonstrate performance monitoring"""
        self.print_header("7. Performance Metrics")
        console.print("[cyan]Retrieving comprehensive performance metrics...[/cyan]")
        
        response = self.client.get("/deep_tree_echo/performance_metrics")
        result = response.json()
        
        self.print_response(result, "Performance Metrics")
        
        # Create summary table
        if "service_metrics" in result:
            table = Table(title="Service Metrics Summary")
            table.add_column("Category", style="cyan")
            table.add_column("Details", style="green")
            
            service = result["service_metrics"]
            table.add_row("Uptime", f"{service.get('uptime_seconds', 0)} seconds")
            table.add_row("Processing Mode", service.get("processing_mode", "unknown"))
            table.add_row("Optimization Level", service.get("optimization_level", "unknown"))
            
            console.print(table)
    
    def run_full_demo(self):
        """Run complete demonstration"""
        console.print(Panel.fit(
            "[bold magenta]Deep Tree Echo FastAPI Endpoints[/bold magenta]\n"
            "[cyan]Interactive Demonstration[/cyan]",
            border_style="magenta"
        ))
        
        try:
            self.demo_health_check()
            time.sleep(1)
            
            self.demo_service_info()
            time.sleep(1)
            
            self.demo_basic_processing()
            time.sleep(1)
            
            self.demo_batch_processing()
            time.sleep(1)
            
            self.demo_streaming()
            time.sleep(1)
            
            self.demo_system_status()
            time.sleep(1)
            
            self.demo_performance_metrics()
            
            # Final summary
            self.print_header("Demo Complete!")
            console.print(Panel(
                "[green]✓ All demonstrations completed successfully![/green]\n\n"
                "[cyan]Key Features Demonstrated:[/cyan]\n"
                "• Health monitoring and service status\n"
                "• Single input DTESN processing with performance metrics\n"
                "• Parallel batch processing for multiple inputs\n"
                "• Real-time streaming capabilities\n"
                "• Comprehensive system information endpoints\n"
                "• Performance monitoring and optimization metrics\n\n"
                "[yellow]Next Steps:[/yellow]\n"
                "• Integrate with your application using the API\n"
                "• Customize configuration for your use case\n"
                "• Monitor performance metrics for optimization\n"
                "• Scale horizontally for production workloads",
                title="[bold green]Summary[/bold green]",
                border_style="green"
            ))
            
        except httpx.ConnectError:
            console.print("[bold red]Error: Could not connect to server[/bold red]")
            console.print("[yellow]Please ensure the server is running:[/yellow]")
            console.print("[cyan]  python3.11 run_deep_tree_echo_server.py[/cyan]")
        except Exception as e:
            console.print(f"[bold red]Error during demo: {e}[/bold red]")
        finally:
            self.client.close()


def main():
    """Main entry point"""
    import sys
    
    # Check for rich library
    try:
        from rich import print as rprint
    except ImportError:
        print("Installing required dependencies...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
        print("Dependencies installed. Please run again.")
        return
    
    # Run demo
    demo = DeepTreeEchoDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main()
