/**
 * RAL SEO — campi SEO per gli articoli di roccoandrealigorio.it
 *
 * Snippet PHP di WPCode (id 213), "Esegui ovunque". Lavora insieme allo snippet
 * "Blog – stile, intestazione e SEO articoli" (id 151), che stampa già meta description
 * (dall'estratto), Open Graph, Twitter card e JSON-LD: qui NON si ripetono quei tag.
 *
 * Cosa aggiunge:
 *  - registra ral_seo_title / ral_seo_description / ral_seo_keyword, scrivibili via API REST
 *    da blog-automatico (restano salvati nell'articolo);
 *  - se ral_seo_title è compilato, lo usa come <title> della pagina dell'articolo.
 */

add_action( 'init', function () {
	foreach ( array( 'ral_seo_title', 'ral_seo_description', 'ral_seo_keyword' ) as $chiave ) {
		register_post_meta( 'post', $chiave, array(
			'type'              => 'string',
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback'     => function () {
				return current_user_can( 'edit_posts' );
			},
		) );
	}
} );

// Dopo lo snippet 151 (priorità 30): il titolo SEO scelto per l'articolo ha la precedenza
add_filter( 'pre_get_document_title', function ( $titolo ) {
	if ( ! is_singular( 'post' ) ) {
		return $titolo;
	}
	$t = get_post_meta( get_queried_object_id(), 'ral_seo_title', true );
	return $t ? $t : $titolo;
}, 40 );
