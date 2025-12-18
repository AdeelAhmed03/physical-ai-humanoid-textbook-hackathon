"""
RAG accuracy validation to ensure responses come from textbook only
"""
from typing import List, Dict, Any
from ..utils.logging_config import logger


def validate_response_accuracy(response: str, query: str, context_used: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate that the response is accurate and based on the provided context
    Returns a validation report with accuracy assessment
    """
    validation_report = {
        "is_accurate": True,
        "confidence_score": 1.0,
        "issues": [],
        "suggestions": []
    }
    
    # Check if the response is empty
    if not response or not response.strip():
        validation_report["is_accurate"] = False
        validation_report["confidence_score"] = 0.0
        validation_report["issues"].append("Response is empty")
        return validation_report
    
    # Check if the response contains hallucinations
    # This is a simplified check - in a real implementation, this would be more sophisticated
    response_lower = response.lower()
    
    # Check for common hallucination indicators
    hallucination_indicators = [
        "according to my training data",
        "i found this information",
        "based on general knowledge",
        "wikipedia says",
        "the internet says"
    ]
    
    for indicator in hallucination_indicators:
        if indicator in response_lower:
            validation_report["is_accurate"] = False
            validation_report["confidence_score"] = 0.2
            validation_report["issues"].append(f"Response contains potential hallucination indicator: '{indicator}'")
            validation_report["suggestions"].append("Ensure the response only references information from the textbook content")
    
    # Check if the response references information not in the provided context
    if context_used:
        context_text = " ".join([item.get("payload", {}).get("text", "") for item in context_used]).lower()
        
        # This is a basic check - in a real implementation, we'd use more sophisticated NLP techniques
        # to determine if the response is supported by the context
        if len(context_text) > 0:
            # Simple check: if the response contains specific technical terms that aren't in context
            # This is a simplified check and would need more advanced NLP in production
            response_words = set(response_lower.split())
            context_words = set(context_text.split())
            
            # Calculate overlap ratio
            if context_words:
                common_words = response_words.intersection(context_words)
                overlap_ratio = len(common_words) / len(response_words)
                
                if overlap_ratio < 0.3:  # If less than 30% of words are in context
                    validation_report["confidence_score"] *= 0.5
                    validation_report["issues"].append(f"Low text overlap with provided context: {overlap_ratio:.2%}")
                    validation_report["suggestions"].append("Ensure the response is more directly based on the textbook content")
    
    # Log the validation result
    logger.debug(f"Response validation result: {validation_report}")
    
    return validation_report


def validate_source_citation(response: str, sources: List[str]) -> bool:
    """
    Validate that the response properly cites sources from the textbook
    """
    # In a simple implementation, we just check if sources were provided
    # A more thorough implementation would verify that the response content 
    # aligns with the cited sources
    
    if not sources:
        logger.warning("Response has no sources cited")
        return False
    
    logger.debug(f"Response cites {len(sources)} source(s)")
    return True


def validate_no_external_knowledge(response: str) -> Dict[str, bool]:
    """
    Validate that the response doesn't contain external knowledge not in the textbook
    """
    validation_result = {
        "no_external_knowledge": True,
        "has_external_knowledge": False,
        "external_indicators": []
    }
    
    # Look for indicators of external knowledge
    external_indicators = [
        "recently in the news",
        "as of 2023", 
        "as of 2024",
        "latest research shows",
        "new studies indicate",
        "breaking news",
        "current events",
        "recent developments"
    ]
    
    response_lower = response.lower()
    for indicator in external_indicators:
        if indicator in response_lower:
            validation_result["no_external_knowledge"] = False
            validation_result["has_external_knowledge"] = True
            validation_result["external_indicators"].append(indicator)
            logger.warning(f"Found potential external knowledge indicator: {indicator}")
    
    return validation_result