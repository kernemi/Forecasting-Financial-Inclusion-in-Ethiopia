"""
Visualization utilities for Ethiopia Financial Inclusion project.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class VisualizationError(Exception):
    """Custom exception for visualization errors."""
    pass


class FinancialInclusionVisualizer:
    """Create visualizations for financial inclusion analysis with robust error handling."""
    
    def __init__(self, style: str = 'whitegrid'):
        """
        Initialize visualizer.
        
        Args:
            style: Seaborn style to use
        """
        try:
            sns.set_style(style)
            plt.rcParams['figure.figsize'] = (12, 6)
        except Exception as e:
            logger.warning(f"Could not set style '{style}': {e}. Using default.")
        
    def _validate_plot_data(self, data: pd.DataFrame, required_cols: List[str], plot_name: str) -> bool:
        """
        Validate data before plotting.
        
        Args:
            data: DataFrame to validate
            required_cols: List of required column names
            plot_name: Name of plot for error messages
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            VisualizationError: If data is invalid
        """
        if data is None:
            raise VisualizationError(f"{plot_name}: Data is None")
        
        if len(data) == 0:
            raise VisualizationError(f"{plot_name}: Data is empty")
        
        missing_cols = set(required_cols) - set(data.columns)
        if missing_cols:
            raise VisualizationError(
                f"{plot_name}: Missing required columns: {missing_cols}"
            )
        
        # Check for all-NA columns
        for col in required_cols:
            if data[col].isna().all():
                raise VisualizationError(
                    f"{plot_name}: Column '{col}' contains only NA values"
                )
        
        return True
    
    def plot_time_series(self, 
                         data: pd.DataFrame, 
                         x_col: str = 'year',
                         y_col: str = 'value_numeric',
                         title: str = 'Time Series',
                         xlabel: str = 'Year',
                         ylabel: str = 'Value',
                         color: str = '#2ecc71',
                         figsize: Tuple[int, int] = (12, 6)) -> Optional[plt.Figure]:
        """
        Plot time series data with robust error handling.
        
        Args:
            data: DataFrame with time series data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            color: Line color
            figsize: Figure size
            
        Returns:
            Matplotlib figure or None if error
            
        Raises:
            VisualizationError: If data validation fails
        """
        try:
            # Validate data
            self._validate_plot_data(data, [x_col, y_col], "Time Series Plot")
            
            # Remove NA values
            plot_data = data[[x_col, y_col]].dropna()
            
            if len(plot_data) == 0:
                raise VisualizationError("No valid data points after removing NAs")
            
            fig, ax = plt.subplots(figsize=figsize)
            
            ax.plot(plot_data[x_col], plot_data[y_col], marker='o', linewidth=2.5, 
                    markersize=8, color=color, label=ylabel)
            
            # Add data labels with error handling
            try:
                for _, row in plot_data.iterrows():
                    if pd.notna(row[y_col]):
                        ax.annotate(f'{row[y_col]:.1f}', 
                                   xy=(row[x_col], row[y_col]),
                                   xytext=(0, 10), textcoords='offset points',
                                   ha='center', fontsize=9, alpha=0.7)
            except Exception as e:
                logger.warning(f"Could not add data labels: {e}")
            
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel(xlabel, fontsize=11)
            ax.set_ylabel(ylabel, fontsize=11)
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            plt.tight_layout()
            return fig
            
        except VisualizationError:
            raise
        except Exception as e:
            raise VisualizationError(f"Error creating time series plot: {e}")
    
    def plot_growth_analysis(self, 
                            growth_data: pd.DataFrame,
                            title: str = 'Growth Rate Analysis',
                            figsize: Tuple[int, int] = (14, 6)) -> Optional[plt.Figure]:
        """
        Plot growth rate analysis with values and rates, with robust error handling.
        
        Args:
            growth_data: DataFrame with year, value_numeric, growth_rate columns
            title: Plot title
            figsize: Figure size
            
        Returns:
            Matplotlib figure or None if error
            
        Raises:
            VisualizationError: If data validation fails
        """
        try:
            # Validate data
            required_cols = ['year', 'value_numeric']
            self._validate_plot_data(growth_data, required_cols, "Growth Analysis Plot")
            
            fig, axes = plt.subplots(1, 2, figsize=figsize)
            
            # Plot 1: Values over time
            plot_data = growth_data[['year', 'value_numeric']].dropna()
            if len(plot_data) == 0:
                raise VisualizationError("No valid data for value plot")
            
            axes[0].plot(plot_data['year'], plot_data['value_numeric'], 
                        marker='o', linewidth=2.5, markersize=8, color='#3498db')
            axes[0].set_title('Value Over Time', fontsize=12, fontweight='bold')
            axes[0].set_xlabel('Year')
            axes[0].set_ylabel('Value (%)')
            axes[0].grid(True, alpha=0.3)
            
            # Plot 2: Growth rates (if available)
            if 'growth_pp' in growth_data.columns:
                growth_plot = growth_data[['year', 'growth_pp']].dropna()
                
                if len(growth_plot) > 0:
                    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in growth_plot['growth_pp']]
                    axes[1].bar(growth_plot['year'], growth_plot['growth_pp'], 
                               color=colors, edgecolor='black', alpha=0.7)
                    axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
                    axes[1].set_title('Year-over-Year Change (pp)', fontsize=12, fontweight='bold')
                    axes[1].set_xlabel('Year')
                    axes[1].set_ylabel('Change (percentage points)')
                    axes[1].grid(True, alpha=0.3, axis='y')
                else:
                    axes[1].text(0.5, 0.5, 'No growth data available', 
                                ha='center', va='center', transform=axes[1].transAxes)
            else:
                axes[1].text(0.5, 0.5, 'Growth data not provided', 
                            ha='center', va='center', transform=axes[1].transAxes)
            
            fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
            plt.tight_layout()
            return fig
            
        except VisualizationError:
            raise
        except Exception as e:
            raise VisualizationError(f"Error creating growth analysis plot: {e}")
    
    def plot_pillar_comparison(self, 
                               pillar_data: pd.DataFrame,
                               figsize: Tuple[int, int] = (14, 8)) -> Optional[plt.Figure]:
        """
        Compare indicators across pillars.
        
        Args:
            pillar_data: DataFrame with pillar comparison data
            figsize: Figure size
            
        Returns:
            Matplotlib figure or None if data is invalid
        """
        # Validate input data
        try:
            self._validate_plot_data(
                pillar_data, 
                required_cols=['pillar'], 
                plot_name='pillar comparison'
            )
        except VisualizationError as e:
            logger.error(f"Pillar comparison validation failed: {e}")
            return None
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=figsize)
            
            # Plot 1: Observations by pillar
            pillar_counts = pillar_data['pillar'].value_counts()
            if len(pillar_counts) > 0:
                axes[0, 0].bar(pillar_counts.index, pillar_counts.values, 
                              color='steelblue', edgecolor='black')
                axes[0, 0].set_title('Observations by Pillar', fontweight='bold')
                axes[0, 0].set_ylabel('Count')
                axes[0, 0].tick_params(axis='x', rotation=45)
                axes[0, 0].grid(True, alpha=0.3, axis='y')
            else:
                axes[0, 0].text(0.5, 0.5, 'No pillar data available', 
                               ha='center', va='center', fontsize=12)
            
            # Plot 2: Indicators by pillar
            if 'indicators' in pillar_data.columns:
                valid_data = pillar_data.dropna(subset=['pillar', 'indicators'])
                if len(valid_data) > 0:
                    axes[0, 1].bar(valid_data['pillar'], valid_data['indicators'],
                                  color='coral', edgecolor='black')
                    axes[0, 1].set_title('Unique Indicators by Pillar', fontweight='bold')
                    axes[0, 1].set_ylabel('Count')
                    axes[0, 1].tick_params(axis='x', rotation=45)
                    axes[0, 1].grid(True, alpha=0.3, axis='y')
            
            # Plot 3: Years coverage
            if 'years_coverage' in pillar_data.columns:
                valid_data = pillar_data.dropna(subset=['pillar', 'years_coverage'])
                if len(valid_data) > 0:
                    axes[1, 0].bar(valid_data['pillar'], valid_data['years_coverage'],
                                  color='#2ecc71', edgecolor='black')
                    axes[1, 0].set_title('Years of Coverage by Pillar', fontweight='bold')
                    axes[1, 0].set_ylabel('Years')
                    axes[1, 0].tick_params(axis='x', rotation=45)
                    axes[1, 0].grid(True, alpha=0.3, axis='y')
            
            # Plot 4: Timeline by pillar
            if 'first_year' in pillar_data.columns and 'last_year' in pillar_data.columns:
                valid_data = pillar_data.dropna(subset=['first_year', 'last_year', 'pillar'])
                if len(valid_data) > 0:
                    for idx, row in valid_data.iterrows():
                        axes[1, 1].plot([row['first_year'], row['last_year']], 
                                       [idx, idx], 'o-', linewidth=3, markersize=8)
                    axes[1, 1].set_yticks(range(len(valid_data)))
                    axes[1, 1].set_yticklabels(valid_data['pillar'])
                    axes[1, 1].set_title('Data Coverage Timeline', fontweight='bold')
                    axes[1, 1].set_xlabel('Year')
                    axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            return fig
            
        except VisualizationError:
            raise
        except Exception as e:
            raise VisualizationError(f"Error creating pillar comparison plot: {e}")
    
    def plot_gender_gap_analysis(self,
                                 gender_data: pd.DataFrame,
                                 figsize: Tuple[int, int] = (12, 6)) -> Optional[plt.Figure]:
        """
        Plot gender gap analysis.
        
        Args:
            gender_data: DataFrame with gender gap data
            figsize: Figure size
            
        Returns:
            Matplotlib figure or None if data is invalid
        """
        # Validate input data
        try:
            self._validate_plot_data(
                gender_data,
                required_cols=['indicator_code', 'year', 'value_numeric'],
                plot_name='gender gap analysis'
            )
        except VisualizationError as e:
            logger.error(f"Gender gap analysis validation failed: {e}")
            return None
        
        try:
            # Remove NA values
            clean_data = gender_data.dropna(subset=['year', 'value_numeric', 'indicator_code'])
            
            if len(clean_data) == 0:
                logger.warning("No valid gender gap data after removing NA values")
                fig, ax = plt.subplots(figsize=figsize)
                ax.text(0.5, 0.5, 'No valid gender gap data available',
                       ha='center', va='center', fontsize=14)
                ax.set_title('Gender Gap in Financial Inclusion Over Time', 
                            fontsize=14, fontweight='bold')
                return fig
            
            fig, ax = plt.subplots(figsize=figsize)
            
            # Plot each indicator
            for indicator in clean_data['indicator_code'].unique():
                data = clean_data[clean_data['indicator_code'] == indicator]
                if len(data) > 0:
                    ax.plot(data['year'], data['value_numeric'], 
                           marker='o', linewidth=2.5, markersize=8, 
                           label=indicator)
            
            ax.set_title('Gender Gap in Financial Inclusion Over Time', 
                        fontsize=14, fontweight='bold')
            ax.set_xlabel('Year', fontsize=11)
            ax.set_ylabel('Gap (percentage points)', fontsize=11)
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            return fig
            
        except VisualizationError:
            raise
        except Exception as e:
            raise VisualizationError(f"Error creating gender gap analysis plot: {e}")
    
    def save_figure(self, fig: plt.Figure, filepath: str, dpi: int = 300):
        """
        Save figure to file.
        
        Args:
            fig: Matplotlib figure
            filepath: Output file path
            dpi: Resolution
        """
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
        print(f"✓ Saved: {filepath}")
